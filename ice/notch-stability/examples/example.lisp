(ql:quickload :cl-mpm/examples/ice-buoyancy)
(in-package :cl-mpm/examples/ice-buoyancy)

(setf *alpha* 1d0)
(defun calving-test (&key (notch-ratio 0d0))
  (cl-mpm/utils::set-workers 4)
  (let* ((mps 3)
         (dt 1d3)
         (total-time 1d10)
         (H 400d0)
         (ice-aspect 6d0)
         (density 918d0)
         (explicit-dt-scale 0.50d0)
         (water-damping 100d0)
         (friction 0.5d0)
         (floatation-ratio 0.9d0)
         (output-dir (format nil "./data/output-~F/" notch-ratio))
         )
    (defparameter *length-scaler* 3d0)
    (setup
     :refine 0.125
     :friction friction
     :bench-length (* notch-ratio H)
     :bench-extra-cut (* 0d0 (* H 1d0))
     :undercut-length (* 0d0 H)
     :ice-height H
     :mps mps
     :hydro-static nil
     :cryo-static t
     :elastic-static  nil
     :melange nil
     :aspect ice-aspect
     :slope 0d0
     :floatation-ratio floatation-ratio
     :use-penalty t
     :stick-base nil)

    (cl-mpm/output:add-mp-output *sim* :SCALAR "eroded"
                                 (lambda (mp)
                                   (/ (cl-mpm/particle::mp-eroded-volume mp) (cl-mpm/particle::mp-mass mp))))

    (cl-mpm/output:add-mp-output *sim* :SCALAR "boundary" #'cl-mpm/particle::mp-boundary)
    (cl-mpm/output:add-mp-output *sim* :SCALAR "plastic-c" #'cl-mpm/particle::mp-c)
    (cl-mpm/output:add-mp-output *sim* :VECTOR "body-force" #'cl-mpm/particle::mp-body-force)
    (cl-mpm/output:add-node-output *sim* :VECTOR "boundary-vec" #'cl-mpm/mesh::node-boundary-vec)

    (cl-mpm::domain-sort-mps *sim*)

    (when (typep *sim* 'cl-mpm/dynamic-relaxation::mpm-sim-octree)
      (setf (cl-mpm/dynamic-relaxation::sim-intra-mesh-aggregation *sim*) t)
      (setf (cl-mpm/dynamic-relaxation::sim-octree-refinement-criteria *sim*)
            (lambda (sim mesh c)
              (or
               (damage-refinement-criteria sim mesh c)))))


    ;(plot-domain)
    ;; (break)

    (setf (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) 0d0)

    (setf (cl-mpm/damage::sim-enable-stress-based-length *sim*) nil)
    (setf (cl-mpm/damage::sim-enable-ekl *sim*) nil)
    (setf (cl-mpm/damage::sim-enable-length-localisation *sim*) t)
    ;; (setf (cl-mpm::sim-nonlocal-damage *sim*) nil)

    (setf (cl-mpm:sim-settings *sim*)
          (list :OCEAN-HEIGHT *water-height*
                :EXPLICIT-DT-SCALE explicit-dt-scale
                :EKL  (cl-mpm/damage::sim-enable-ekl *sim*)
                :LENGTH-LOCALISATION  (cl-mpm/damage::sim-enable-length-localisation *sim*)
                :PLASTIC-DAMAGE-DRIVING *enable-plastic-damage*
                :PLASTIC-DAMAGE-OVERSIZE *pd-oversize*
                :DELAY-TIME *delay-time*
                :DELAY-EXP *delay-exponent*
                :ANGLE *angle*
                :ANGLE-R *angle-r*
                :ANGLE-PSI *angle-psi*
                :WATER-DAMPING water-damping
                :R-C *rc*
                :GF *gf*
                :LENGTH-SCALER *length-scaler*
                :TENSILE-STRENGTH *tensile-strength*))

    (setf (cl-mpm:sim-enable-damage *sim*) nil)

    (cl-mpm/setup::set-mass-filter *sim* 918d0 :proportion 1d-15)

    ;; (break)
    (loop for f in (uiop:directory-files (uiop:merge-pathnames* "./outframes/")) do (uiop:delete-file-if-exists f))
    (let ((step 0)
          (substeps (ceiling (* 10 (floor H 100) (/ 10d0 (cl-mpm/mesh::mesh-resolution (cl-mpm:sim-mesh *sim*))))))
          )
      (format t "Substeps ~D~%" substeps)
      ;; (setf (cl-mpm/penalty::bc-penalty-friction *floor-bc*) 0d0)

      (cl-mpm/dynamic-relaxation::run-multi-stage
       *sim*
       :output-dir output-dir
       :dt dt
       :conv-dt-scale 0.9d0
       :dt-scale 0.9d0
       :damping-factor (sqrt 2d0)
       :conv-criteria 1d-3
       :conv-load-steps 1
       ;; :min-adaptive-steps -4
       ;; :max-adaptive-steps 10
       :min-adaptive-steps -14
       :max-adaptive-steps 14
       :adaption-constant 4
       :easy-step-adaption-constant 4
       :max-damage-inc 1.9d0
       :min-tangent-ratio 1d-2
       :max-inertia-norm 1d-4
       :max-deformation-gradient 4d0

       :max-plastic-inc nil
       :stagger-damage :HYBRID-FULL
       :substeps substeps
       :sub-conv-steps 500
       :total-time total-time
       :save-vtk-loadstep t
       :save-vtk-dr nil
       :enable-plastic t
       :enable-damage t
       :plotter (lambda (sim) (incf step))
       :explicit-conv-criteria 1d-3
       :elastic-dt-margin 1d2
       :explicit-mass-scaling nil
       :explicit-damping-factor 1d-3
       :explicit-dt-scale explicit-dt-scale
       :explicit-dynamic-solver 'cl-mpm/damage::mpm-sim-agg-damage

       :post-conv-step
       (lambda (sim)
         ;; (cl-mpm::domain-sort-mps *sim*)
         (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) water-damping
         (setf (cl-mpm/bc::bc-enable *bc-erode*) nil))
       :setup-quasi-static
       (lambda (sim)
         ;(cl-mpm/setup::set-mass-filter *sim* 918d0 :proportion 1d-15)
         (setf
          (cl-mpm::sim-velocity-algorithm sim) :QUASI-STATIC
          )
         (when (typep *sim* 'cl-mpm/dynamic-relaxation::mpm-sim-dr-dynamic)

           (setf (cl-mpm/dynamic-relaxation::sim-true-damping *sim*) (* 0d-6 (cl-mpm/setup::estimate-critical-damping *sim*))
                 (cl-mpm::sim-velocity-algorithm sim) :TBLEND
                 ))
         ;; (cl-mpm::remove-mps-func
         ;;  *sim*
         ;;  (lambda (mp)
         ;;    (and
         ;;     (typep mp 'cl-mpm/particle::particle-damage)
         ;;     (> (cl-mpm/particle::mp-damage mp) 0.9d0))))
         ;; (cl-mpm::reset-grid (cl-mpm:sim-mesh *sim*) :reset-displacement t)
         ;; (cl-mpm/dynamic-relaxation::pre-step *sim*)
         ;; (cl-mpm::check-mps *sim*)
         (setf
          (cl-mpm/penalty::bc-penalty-friction *floor-bc*) friction
          (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) water-damping))
       :setup-dynamic
       (lambda (sim)
         ;(cl-mpm/setup::set-mass-filter *sim* 918d0 :proportion 1d-15)
         (setf
          (cl-mpm/damage::sim-damage-delocal-counter-max sim) 2
          (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) water-damping
          (cl-mpm::sim-velocity-algorithm sim) :TBLEND))))))


(let ((ratio (parse-float:parse-float (uiop:getenv "NOTCH"))))
  (calving-test :notch-ratio ratio))
