Finite beta (plasma averaged beta of 0.89%), finite current, multi-volume, free-boundary SPEC equilibrium in a simple geometry (rotating ellipse) and with coils.

* _ellipse.coils_ contains the coils geometry. These were obtained with FOCUS; I tried to find coils that generate a flux surface at the computational boundary (Rwc, Zws in Input.sp) in vacuum.
* _focus_\_ _ellipse.sp_ contains the full Fourier harmonics of the external field projected on the computational boundary normal direction, _i.e._ the `Vns` harmonics.
* _Input.sp_ is the SPEC input file using a non-zero pressure and interface current profile. Initial guess for the inner plasma interfaces is provided as well.

