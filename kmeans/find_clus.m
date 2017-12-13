function [segs]=find_clus(name,groundTruth)
    segs=0;
    best=0;
    for k=1:3
        seg=AllFunctions.segmentate(name,k);
        segs={seg};
        y=sum(sum(match_segmentations(seg, groundTruth)));
        if y>best
            segs=seg;
            best=y;
        end
    end

    