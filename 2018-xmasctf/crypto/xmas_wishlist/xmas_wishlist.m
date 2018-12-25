trainedLanguage = 'path_to_tessdata_folder/xmas.traineddata';
layout = 'Block';

f = fopen('results.txt','w');

I = imread('wishlist.png');
results = ocr(I, ...
        'Language', trainedLanguage, ...
        'TextLayout', layout);

fprintf(f, results.Text);
fclose(f);