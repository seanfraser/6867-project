 
 srcFiles = dir('BSD500CNN_out_morph/*.jpg');  % the folder in which ur images exists
 for i = 1 : length(srcFiles)
     filename = strcat('BSD500CNN_out_morph/',srcFiles(i).name);
     Im = imread(filename);
     S = L0Smoothing(Im,0.01);
     %figure, imshow(S);
     newfilename = strcat('BSD500CNN_out_morph_L0/',srcFiles(i).name(1:end-14));
     imwrite(S,strcat(newfilename,'.jpg'));
 end