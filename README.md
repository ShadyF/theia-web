
# [Theia-Web](https://theia-web.herokuapp.com/editor/)
Theia-Web, a continuiation of [Theia](https://github.com/ShadyF/Theia), is an web-based image manipulation tool that allows its users to edit their images, on the fly, from their browsers.

This tool was made using Python's [Django](https://www.djangoproject.com/) web framework.

Try it out at https://theia-web.herokuapp.com/editor/!

## What Theia offers
- Transformations
- Color Tints
- Color Filters (Same as the ones used in Instagram/Snapchat)
- Adjustments/Enhancements
- Kernel Filters
- Drawing

## Usage
- Open https://theia-web.herokuapp.com/editor/
- Click on the Browse button on the left.
- Choose the image to be manipulate.
- Wait until the image has been uploaded to the server.
- Apply some transformation/filters or do some drawing.
- Press the Download Button to download the image.

## Browser Support
Theia was tested succesfully on Chrome, Firefox, Safari and Android Browser.

## Dependencies
- Backend
  - Python 3.4
  - Django 1.9.7
  - Pillow 3.2.0
  - [ImageMagick](http://www.imagemagick.org/script/index.php) binaries 6.7.7-10
- Frontend
  - Jquery 1.12.4
  - Twitter Bootstrap 3.3.4
  - [J I C (Javascript Image Compressor)](https://github.com/brunobar79/J-I-C)
  - Edited version of [jqScribble](https://github.com/jimdoescode/jqScribble)

## TODO List
- Allow users to sign up/login and save their images online.
- Pick a specific color (RGB) when applying tints instead of the preset ones.
- Add more transformations (Shearing, Translation, etc...)
- Add more adjustments (Gamma, Saturation, etc...)
- Add an undo button.

## How it works
Theia, from ground up, was built to allow its back-end server to do all the heavy lifting when it comes to image processing. In other words, no processing is done on the client/browser side, almost everything is off-loaded to the back-end server.

Once the user chooses the image he wished to edit, the image is compressed and uploaded to the back-end server where it is stored for the user's current session.

Each time a user requests an operation, the already stored image on the server side is processed and resent to the user, i.e the user has to download his image, after processing, each time he request an operation. This would arguably lead to slow response time if the image's original size is too large and the user's internet connection isn't fast enough.

## Credits
A huge thank you to [TheAbaza](https://github.com/TheAbaza) and [ychamel](https://github.com/ychamel) for the name.
