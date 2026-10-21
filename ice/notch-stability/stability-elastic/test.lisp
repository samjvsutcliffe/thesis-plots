(in-package :cl-mpm/examples/ice-buoyancy)
(defun calving-test (&key (output-dir "./output/") (H 600d0)
                       (refine 0.125)
                       (debug t)
                       (erode t)
                       (aspect 4d0)
                       (bench-ratio 0d0)
                       )
  (let* ((mps 3)
         (dt 1d3)
         (total-time 1d10)
         (ice-aspect aspect)
         (density 918d0)
         (explicit-dt-scale 0.25d0)
         (water-damping 10d0)
         (friction 0.5d0)
         (floatation-ratio 0.9d0))
    (defparameter *length-scaler* 3d0)
    (setup
     :refine refine
     :friction friction
     :bench-length (* bench-ratio H)
     :bench-extra-cut (* 0d0 (* H 1d0))
     :undercut-length (* 0d0 H)
     :ice-height H
     :mps mps
     :hydro-static nil
     :cryo-static nil
     :elastic-static t
     :melange nil
     :aspect ice-aspect
     :slope 0d0
     :floatation-ratio floatation-ratio
     :use-penalty t
     :stick-base nil)

    (cl-mpm::domain-sort-mps *sim*)
    (setf (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) 0d0)
    (setf (cl-mpm/damage::sim-enable-stress-based-length *sim*) nil)
    (setf (cl-mpm/damage::sim-enable-ekl *sim*) nil)
    (setf (cl-mpm/damage::sim-enable-length-localisation *sim*) t)

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
    (reduced-output-data *sim*)
    ;; (setup-settings)

    (let ((step 0)
          (substeps (ceiling (* 10 (floor H 100) (/ 10d0 (cl-mpm/mesh::mesh-resolution (cl-mpm:sim-mesh *sim*)))))))
      (format t "Substeps ~D~%" substeps)
      (cl-mpm/dynamic-relaxation::run-multi-stage
       *sim*
       :output-dir output-dir
       :dt dt
       :conv-dt-scale 0.9d0
       :dt-scale 0.9d0
       :damping-factor (sqrt 2d0)
       :conv-criteria 1d-2
       :conv-load-steps 1
       :min-adaptive-steps -20
       :max-adaptive-steps 20
       :adaption-constant 2
       :easy-step-adaption-constant 4
       :max-damage-inc 0.9d0
       :min-tangent-ratio 1d-1
       :max-deformation-gradient 2d0
       :max-plastic-inc nil
       ;; :max-inertia-norm 1d-3
       :stagger-damage :HYBRID-FULL
       :substeps substeps
       :sub-conv-steps 500
       :total-time total-time
       :save-vtk-loadstep t
       :save-vtk-dr nil
       :enable-plastic t
       :enable-damage t
       :plotter (lambda (sim))
       :explicit-conv-criteria 1d-3
       :elastic-dt-margin 1d2
       :explicit-mass-scaling nil
       :explicit-damping-factor 1d-4
       :explicit-dt-scale explicit-dt-scale
       :explicit-output-frequency 1
       :explicit-dynamic-solver 'cl-mpm/damage::mpm-sim-agg-damage
       :post-conv-step
       (lambda (sim)
         (setf (cl-mpm/bc::bc-enable *bc-erode*) erode)
         (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) water-damping)
       :setup-quasi-static
       (lambda (sim)
         (setf
          (cl-mpm::sim-velocity-algorithm sim) :QUASI-STATIC)
         (setf
          (cl-mpm/penalty::bc-penalty-friction *floor-bc*) friction
          (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) water-damping))
       :setup-dynamic
       (lambda (sim)
         (setf
          (cl-mpm/damage::sim-damage-delocal-counter-max sim) 2
          (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) water-damping
          (cl-mpm::sim-velocity-algorithm sim) :TBLEND))))))

(defun calving-qs-test (&key (output-dir "./output/") (H 600d0)
                          (erode nil)
                          (bench-ratio 0d0)
                          (refine 0.25)
                          (debug t)
                          (aspect 4d0)
                          )
  (format t "Testing ~A~%" output-dir)
  (let* ((mps 3)
         (density 918d0)
         (water-damping 0d0))
    (defparameter *length-scaler* 3d0)
    (setup :refine refine
           :friction 0.5d0
           :bench-length (* bench-ratio H)
           :bench-extra-cut 00d0
           :ice-height H
           :mps mps
           :hydro-static nil
           :cryo-static nil
           :elastic-static t
           :melange nil
           :aspect aspect
           :slope 0.0d0
           :floatation-ratio 0.90d0
           :use-penalty t
           ;; :stick-base t
           )
    (change-class *sim* 'cl-mpm/dynamic-relaxation::mpm-sim-dr-dynamic)
    (unless debug
      (reduced-output-data *sim*))
    (setup-settings)
    (setf (cl-mpm/buoyancy::bc-viscous-damping *water-bc*) water-damping)
    (setf (cl-mpm/damage::sim-enable-ekl *sim*) nil)
    (setf (cl-mpm/damage::sim-enable-length-localisation *sim*) t)
    (setf (cl-mpm:sim-enable-damage *sim*) t)
    (cl-mpm/setup::set-mass-filter *sim* 918d0 :proportion 1d-15)
    (loop for f in (uiop:directory-files (uiop:merge-pathnames* "./outframes/")) do (uiop:delete-file-if-exists f))
    (setf (cl-mpm::sim-velocity-algorithm *sim*) :TBLEND)
    ;; (setf (cl-mpm/dynamic-relaxation::sim-enable-dynamics *sim*) nil)
    (let ((step 0)
          (substeps (ceiling (* 10 (floor H 100) (/ 10d0 (cl-mpm/mesh::mesh-resolution (cl-mpm:sim-mesh *sim*))))))
          (elastic-dt (cl-mpm/setup::estimate-elastic-dt *sim*)))
      (format t "Substeps ~D~%" substeps)
      (cl-mpm/dynamic-relaxation::run-quasi-time
       *sim*
       :output-dir output-dir
       :dt 1d4
       :total-time 1d10
       :dt-scale 0.9d0
       :enable-plastic t
       :enable-damage t
       :substeps substeps
       :sub-conv-steps 500
       :min-adaptive-steps -14
       :max-adaptive-steps 14
       :adaption-constant 4
       :adaption-easy-steps 4
       :max-damage-inc 0.5d0
       :max-plastic-inc nil
       :max-deformation-gradient 4d0
       :min-tangent-ratio 1d-1
       :conv-criteria 1d-3
       :save-vtk-loadstep t
       :save-vtk-dr nil
       :elastic-solver 'cl-mpm/dynamic-relaxation::mpm-sim-quasi-static
       :initial-quasi-static t
       :post-conv-step
       (lambda (sim)
         (setf (cl-mpm/bc::bc-enable *bc-erode*) erode)
         (when (typep *sim* 'cl-mpm/dynamic-relaxation::mpm-sim-dr-dynamic)
             (setf (cl-mpm/dynamic-relaxation::sim-true-damping *sim*) (* 1d-3 (cl-mpm/setup::estimate-critical-damping *sim*))))
         (setf
          (cl-mpm/aggregate::sim-enable-aggregate *sim*) t
          (cl-mpm::sim-ghost-factor *sim*) nil))
       :plotter (lambda (sim)
                  (format t "~A ~%" (local-time:now)))
       :post-load-step (lambda (sim) (incf step))))))

(defun plot-domain (sim))


(defparameter *tensile-strength* 0.1d6)
(defparameter *biot-coefficent* 1d0)
(defparameter *alpha* 0.5d0)
(defparameter *ductility* 10d0)
(defparameter *delay-time* 1d5)
(defparameter *delay-exponent* 2d0)
(defparameter *angle* 38d0)
(defparameter *angle-r* 38d0)
(defparameter *angle-psi* 5d0)
(defparameter *rt* (- 1d0 1d-2))
(defparameter *pd-oversize* 1d-2)
(defparameter *enable-viscosity* nil)
(defparameter *rc* (- 1d0 *pd-oversize*))
(defparameter *viscoplastic-hardening* 0d2)

(let* (;; (H (float (parse-float:parse-float (uiop:getenv "HEIGHT")) 0d0))
       ;; (top-dir "./data/")
       (top-dir "/mnt/c/Temp/mici-notch/elastic/")
       (H 400d0)
       (erode nil)
       ;; (refine (* 1d0 (/ 100d0 H)))
       (refine 0.25d0)
       (ratio (parse-float:parse-float (uiop:getenv "NOTCH")))
       )
  ;; (calving-test :output-dir (format nil "./output-erode_~A_~F/" erode H)
  ;;                  :H H
  ;;                  :erode erode
  ;;                  :debug nil
  ;;                  :refine (* 1d0 (/ 100d0 H)))
  (format t "Refine ~E~%" refine)
  (cl-mpm/utils:set-workers 1)
  (calving-test :output-dir (merge-pathnames (format nil "./data/output-~F/" ratio) top-dir)
                   :H H
                   :bench-ratio ratio
                   :erode erode
                   :debug nil
                   :aspect 6d0
                   :refine refine)
  )

(sb-ext:quit)
