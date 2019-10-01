# Face Detection Example
#
# This example shows off the built-in face detection feature of the OpenMV Cam.
#
# Face detection works by using the Haar Cascade feature detector on an image. A
# Haar Cascade is a series of simple area contrasts checks. For the built-in
# frontalface detector there are 25 stages of checks with each stage having
# hundreds of checks a piece. Haar Cascades run fast because later stages are
# only evaluated if previous stages pass. Additionally, your OpenMV Cam uses
# a data structure called the integral image to quickly execute each area
# contrast check in constant time (the reason for feature detection being
# grayscale only is because of the space requirment for the integral image).

import sensor, time, image, gc, pyb, ustruct

usb = pyb.USB_VCP()
led = pyb.LED(1)

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(3)
sensor.set_gainceiling(16)
# HQVGA and GRAYSCALE are the best for face tracking.
sensor.set_framesize(sensor.VGA)
sensor.set_pixformat(sensor.RGB565)
sensor.set_windowing([500,300])

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)

num_faces = 0

while (True):
    # Capture snapshot
    img = sensor.snapshot()

    # Find objects.
    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.60, scale_factor=1.15)

    if num_faces == len(objects):
        continue
    else:
        num_faces = len(objects)

    # Send full image over USB
    for r in objects:
        led.on()
        tmp_fb = sensor.alloc_extra_fb(r[2], r[3], sensor.RGB565)
        send_img = img.copy(r,copy_to_fb=tmp_fb).compress()
        usb.send(b"IMGS")
        usb.send(ustruct.pack("<L", send_img.size()))
        usb.send(send_img)
        usb.send(b"IMGE")
        sensor.dealloc_extra_fb()
        img.draw_rectangle(r)
        led.off()
