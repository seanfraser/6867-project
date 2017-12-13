function [segs]=find_segs(edgemap,groundTruth)
segs=0;
best=0;
best_t=0;
best_f=0;
for thresh=0:8
    for fill=0:8
        mapi=double(edgemap);
        mapi=mapi./255;
        mapi=(mapi>=0.1*thresh);
        mapi=double(bwmorph(mapi, 'thin', fill));
        segments=bwlabel(mapi,4);
        seg=imfill(segments,'holes');
        seg=mat2gray(seg);
        seg=seg.*255;
        seg=round(seg);
        imshow(seg,[]);
        y=sum(sum(match_segmentations(seg, groundTruth)));
        if y>best
            segs=seg;
            best=y;
            best_t=thresh;
            best_f=fill;
        end
        seg1=bwlabel(mapi,8);
        seg1=imfill(seg1,'holes');
        seg1=mat2gray(seg1);
        seg1=seg1.*255;
        seg1=round(seg1);
        imshow(seg1,[]);
        y=sum(sum(match_segmentations(seg1, groundTruth)));
        if y>best
            segs=seg1;
            best=y;
            best_t=thresh;
            best_f=fill;
        end
        
    end
end
        