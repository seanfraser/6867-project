function segAll()
    myFile = dir('In/*.jpg');
    for i = 1 : length(myFile)
        filename = myFile(i).name;
        disp(filename);
        name=strcat('In/',myFile(i).name);
        edgemap=imread(name);
        gr1=strcat('gr/',myFile(i).name);
        gr2=extractBefore(gr1,'.jpg');
        gr=strcat(gr2,'.mat');
        ground=load(gr);
        seg=find_segs(edgemap,ground.groundTruth);
        segs={seg};
        t1=strcat('Ins2/',myFile(i).name);
        t2=extractBefore(t1,'.jpg');
        t=strcat(t2,'.mat');
        k1=strcat('Inm2/',myFile(i).name);
        k2=extractBefore(k1,'.jpg');
        k3=strcat(k2,'.png');
        save(t,'segs');
        imwrite(mat2gray(seg),k3);
    end