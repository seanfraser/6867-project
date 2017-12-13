classdef AllFunctions
    methods(Static)
        function [x,y]=a
            fprintf("k");
            x=1;
            y=3;
        end
        
        function [x] =segmentate(name,k)
        he = imread(name);
        text(size(he,2),size(he,1)+15,...
        'Image courtesy of Alan Partin, Johns Hopkins University', ...
         'FontSize',7,'HorizontalAlignment','right');
        cform = makecform('srgb2lab');
        lab_he = applycform(he,cform);
        ab = double(lab_he(:,:,2:3));
        nrows = size(ab,1);
        ncols = size(ab,2);
        ab = reshape(ab,nrows*ncols,2);
        nColors = k;
        % repeat the clustering 3 times to avoid local minima
        [cluster_idx, cluster_center] = kmeans(ab,nColors,'distance','sqEuclidean', ...
                                      'Replicates',10);
        pixel_labels = reshape(cluster_idx,nrows,ncols);

        x = pixel_labels;
        end 
        
        function [x, y]= convert(segmented,k,filename)
            maxF=0;
            x=[0,0];
            for i=1:k
                normalized=segmented/i;
                predicted=arrayfun(@(a) Average.binary(a),normalized);
                name=extractBefore(filename,".jpg");
                name=extractAfter(name,'867Project/');
                real=Average.ground(name);
                score=Error.Fmeasure(predicted,real);
                if score>maxF
                    maxF=score;
                    x=predicted;
                    y=maxF;
                end
            end  
        end

        function [x, y]= convert1(segmented,filename)
            maxF=0;
            x=[0,0];
            l=segmented(1,4);
            normalized=segmented/l;
                predicted=arrayfun(@(a) Average.binary(a),normalized);
                name=extractBefore(filename,".jpg");
                name=extractAfter(name,'867Project/');
                real=Average.ground(name);
                score=Error.Fmeasure(predicted,real);
                if score>maxF
                    maxF=score;
                    x=predicted;
                    y=maxF;
                end 
            
        end
        
        function [x,name,f, ks]=alldata(max)
            myFile = dir('867Project/*.jpg');
            ks=cell(1, length(myFile));
            x=cell(1, length(myFile));
            name= cell(1, length(myFile));
            f=cell(1, length(myFile));
            for i = 1 : length(myFile)
            filename = strcat('867Project/',myFile(i).name);
            disp(filename);
            maxF=0;
                for k = 2: max
                    segmented=AllFunctions.segmentate(filename,k);
                    [y, z]=AllFunctions.convert1(segmented,filename);
                    if z>maxF
                        maxF=z;
                        name{i}=filename;
                        f{i}=z;
                        x{i}=y;
                        ks{i}=k;
                    end
                end
            end
        end
    end
 end
