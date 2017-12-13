function kAll()
    myFile = dir('L0_croppped/*.jpg');
    for i = 1 : length(myFile)
        filename = myFile(i).name;
        disp(filename);
        name=strcat('Im/',myFile(i).name);
        gr1=strcat('gr/',myFile(i).name);
        gr2=extractBefore(gr1,'.jpg');
        gr=strcat(gr2,'.mat');
        ground=load(gr);
        seg=find_clus(name,ground.groundTruth);
        segs={seg};
        t1=strcat('In/',myFile(i).name);
        t2=extractBefore(t1,'.jpg');
        t=strcat(t2,'.mat');
        save(t,'segs');
        k1=strcat('k_re/',myFile(i).name);
        k2=extractBefore(k1,'.jpg');
        k3=strcat(k2,'.png');
        imwrite(mat2gray(seg),k3);
    end