import pyrealsense2 as rs
import numpy as np
import cv2

## Mapping of color pixel with corresponding depth pixel to localise feature in camera co ordinates

def GetWorldCoordinates(color_pixel,mode):

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
       
    # Start streaming
    pipeline.start(config)

    # Aligning depth frame to color frame
    align = rs.align(rs.stream.color)
    
    for i in range(60):
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        # Aligning depth frame to color frame
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
        depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
        
        # measuring depth in metres at pixel(x,y)

        if mode == "macro":
            # depth = depth_frame.get_distance(color_pixel[0],color_pixel[1])
            depth = 0.470
        
        if mode == "micro":
            depth = 0.172

        # Projecting pixel to world coordinates at measured depth
        # Projected points are wrt camera coordinate frame
        projection = rs.rs2_deproject_pixel_to_point(depth_intrinsics, color_pixel, depth)

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)


        key = cv2.waitKey(1)
                
        # if key & 0xFF == ord('q') or key == 27:
        if i == 29:
            cv2.destroyAllWindows()
            break
        
    pipeline.stop()

    return (projection[0], projection[1], depth)