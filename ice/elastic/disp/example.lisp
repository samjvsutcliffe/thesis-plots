(ql:quickload :cl-mpm/examples/ice-buoyancy)
(in-package :cl-mpm/examples/ice-buoyancy)

(defun initial-stress ()
  (cl-mpm/utils::set-workers 16)
  (let ((output-dir "./output/"))
    (ensure-directories-exist output-dir)
    (loop for f in (uiop:directory-files (uiop:merge-pathnames* output-dir)) do (uiop:delete-file-if-exists f))
    (dolist (initial-stress (list
                             ;; :CRYO-STATIC
                             ;; :ELASTIC-STATIC
                             :NONE
                                  ))
      (dolist (stick (list t nil))
        (let* ((mps 3)
               (output-dir (format nil "./data/output-stress_~A_stick_~A/" initial-stress stick))
               (H 300d0)
               (ice-aspect 4d0)
               (floatation-ratio 0.7d0))
          (defparameter *alpha* 0d0)
          (defparameter *length-scaler* 1d0)
          (format t "Running ~A~%" output-dir)
          (setup
           :refine 0.5
           :friction 0d0
           :bench-length (* 0d0 H)
           :bench-extra-cut (* 0d0 (* H 1d0))
           :ice-height H
           :mps mps
           :cryo-static (equal initial-stress :CRYO-STATIC)
           :elastic-static (equal initial-stress :ELASTIC-STATIC)
           :melange nil
           :aspect ice-aspect
           :slope 0d0
           :floatation-ratio floatation-ratio
           :use-penalty nil
           :stick-base stick)
          (setf
           (cl-mpm:sim-settings *sim*)
           (list :OCEAN-HEIGHT *water-height*))
          ;; (setf (cl-mpm/dynamic-relaxation::dt-loadstep *sim* 0d0))
          (cl-mpm/dynamic-relaxation::run-load-control
           *sim*
           :crit 1d-6
           :output-dir output-dir
           :load-steps 2
           :loading-function (lambda (p))
           :enable-damage nil
           :enable-plastic nil
           :dt-scale 0.9d0
            :post-iter-step
            (lambda (i o e)
              (setf (cl-mpm::sim-enable-damage *sim*) t)
              (cl-mpm/damage:calculate-damage *sim* 1d-15)
              (setf (cl-mpm::sim-enable-damage *sim*) nil)))
          (setf (cl-mpm::sim-enable-damage *sim*) t)
          (cl-mpm/damage:calculate-damage *sim* 1d0)
          (cl-mpm/dynamic-relaxation::save-vtks *sim* output-dir 1)
          (plot-domain)
          (vgplot:title output-dir)
          )))))

(initial-stress)
