 
 srcFiles = dir('average_superpixels/*.png');  % the folder in which ur images exists
 for i = 1 : length(srcFiles)
     filename = strcat('average_superpixels/',srcFiles(i).name);
     Im = imread(filename);
     new_im = adaptcluster_kmeans(Im);
     segs = {new_im};
     save(strcat(strcat('output_average_superpixels/',srcFiles(i).name(1:end-4)),'.mat'),'segs');
 end
 