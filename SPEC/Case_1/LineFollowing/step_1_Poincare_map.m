function step_1_Poincare_map

%surfaces_to_make = 1:101;
surfaces_to_make = 1:121

num_surfs_to_make = length(surfaces_to_make);


parfor ii = 1:num_surfs_to_make
    this_surface = surfaces_to_make(ii);
    
     try
         generate_flux_surfaces(this_surface)
     catch
         disp(['<---Error on surf #' num2str(this_surface)]);
     end
 end
 