# **BlogToVlogPy**

## **Introduction**

**BlogToVlogPy** is an innovative Python application that leverages the OpenAI API to transform textual content, such as blogs, into engaging video files.

## **Features**

- **Text Segmentation**: The application intelligently segments the input text by paragraphs, ensuring a coherent flow in the video narration.
- **Text-to-Speech Conversion**: Utilizing OpenAI's advanced TTS (Text-to-Speech) capabilities, BlogToVlogPy converts each paragraph into lifelike, natural-sounding speech.
- **Image Generation with DALL-E**: For each paragraph, the app generates a unique image using OpenAI's DALL-E. This process involves creating a detailed prompt derived from the text, which is then used to produce a visually appealing and relevant image.
- **Quality Control**: To maintain the quality of the video, the application checks each generated image for non-diegetic text. If such text is detected, the image is rejected and a new one is generated, preventing any irrelevant or misspelled text from appearing in the final video.
- **Video Compilation**: The app seamlessly compiles the narrated audio and corresponding images into a cohesive and polished video, ready for sharing or uploading.

## **How It Works**

BlogToVlogPy transforms your written content into a dynamic, audio-visual experience, making it perfect for platforms like YouTube. By combining state-of-the-art text-to-speech and image generation technologies, it offers an automated solution to create visually captivating and narratively engaging videos from blogs or similar texts.

## **Use**

**RENDER_VIDEO**

OpenAI image generation can get expensive with longer projects. A new image is generated with each paragraph. You can set this flag to false to keep images from generating.

**PLAY_SOUND**

If you want to preview the audio, set this flag to true.

**SHOW_IMAGES**

If you want to preview the images, set this flag to true.

**SKIP_TO_SHOW_GENERATED_IMAGES**

Skip over existing images to show the images that are currently being generated. (To start in the middle of a project.)

**SKIP_TO_PLAY_GENERATED_AUDIO**

Skip to over existing audio and only play the audio thats being generated.

**paragraph_delineator = "\\n\\n"**

You may need to change how it recognizes different paragraphs to suit your text. You also might want to consider reviewing and editing your text to avoid too small or too large of paragraphs for your liking.

**text_file = "input.txt"**

The text you want to convert

**speech_file_path = "./audio/"**

This is where the audio files will be placed, numbered 0.mp3 for the first one and counting up.

**image_file_path = "./images/"**

This is the path for image files, numbered 0.png for the first one and counting up.

**Image Dimentions**

screen_width = 1792

screen_height = 1024

OpenAI will only generate a limited set of image dimentions, your options are:

1024x1024

1024x1792

1792x1024

### **Adding an into image and video**

This could be more elegant, but as of right now, if you'd like to add a sound and image to the beginning of your video, such as a logo, you'll need to do it this way.

1.  Add a dummy paragraph to the beginning of your text. This can be anything, it will be ignored.
2.  Name your audio file 0.mp3 and add it to the directory defined in 'speech_file_path', you may have to create it if you haven't run the program yet.
3.  Name your logo or intro image 0.png and add it to the directory defined in 'image_file_path', you may have to create this as well.
4.  Double check flags are set how you prefer. If you want to preview your intro, set 'SKIP_TO_SHOW_GENERATED_IMAGES' and 'SKIP_TO_PLAY_GENERATED_AUDIO' are set to false.
5.  Run the program.

The program will detect the 0.mp3 and 0.png programs exist and skip over them, and it will also skip over the first paragraph.

### **Editing**

You can stop and start the program, and it will continue from where it was at in the process.

If you don't like an image, you can delete it, rerun the program, and it will generate a new one. You can replace images with your own and it will use them in the video.

If the text isn't being read correctly, you can delete the audio file, change the text to emphasize the correct reading, and rerun the program. So long as you don't change the number of paragraphs before where it is in the process, or you'll have to delete all the audio and images after the paragraph you added and rerun the program. Alternatively, you could renumber the files adding one and the program fill in the missing number, but that could be easy to mess up.
