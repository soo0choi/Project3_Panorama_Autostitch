import time
from math import floor
import numpy as np
import cv2
from scipy.sparse import csr_matrix
import util_sweep


def compute_photometric_stereo_impl(lights, images):
    """
    Given a set of images taken from the same viewpoint and a corresponding set
    of directions for light sources, this function computes the albedo and
    normal map of a Lambertian scene.

    If the computed albedo for a pixel has an L2 norm less than 1e-7, then set
    the albedo to black and set the normal to the 0 vector.

    Normals should be unit vectors.

    Input:
        lights -- N x 3 array.  Rows are normalized and are to be interpreted
                  as lighting directions.
        images -- list of N images.  Each image is of the same scene from the
                  same viewpoint, but under the lighting condition specified in
                  lights.
    Output:
        albedo -- float32 image. When the input 'images' are RGB, it should be of dimension height x width x 3,
                  while in the case of grayscale 'images', the dimension should be height x width x 1.
        normals -- float32 height x width x 3 image with dimensions matching
                   the input images.
    """
    # Create I a vector of N images from the list images by reshaping such
    # that each image is an array of size 1980*1080*c with c=3 for RGB or 1 for greyscale
    images_shape = np.shape(images)

    # ---------------------------
    # TODO 1-1: images 리스트를 (N, H*W*C) 형태의 행렬 I로 변환
    # ---------------------------
    I = ___

    # Compute the product of L transpose and L; then get it inverse 
    # ---------------------------
    # TODO 1-2: L^T L 의 역행렬 계산
    # ---------------------------
    L_t_L_inv = ___

    # Compute the product of L transpose and I 
    # ---------------------------
    # TODO 1-3: L^T I 계산
    # ---------------------------
    L_t_I = ___

    # Compute G
    # ---------------------------
    # TODO 1-4: G = (L^T L)^(-1) (L^T I)
    # ---------------------------
    G = ___

    # Albedo
    # Reshape the image back from an array of 1980x1080xc to an array of 3 dimensions
    # Get the norm
    G_shape = [G.shape[0]]
    G_shape.extend(images_shape[1:])
    G_albedo = G.reshape(G_shape)

    # ---------------------------
    # TODO 2-1: albedo = 각 픽셀별 L2 norm (채널 방향으로 norm)
    # ---------------------------
    albedo = ___

    # Normals
    # Use the norm after getting an average on all the colors and divide the norm
    # by G
    G_shape = []
    G_shape.extend(images_shape[1:])
    G_shape.append(3)

    # ---------------------------
    # TODO 2-2: G를 (H, W, 3, C)로 보고 채널 방향 평균을 내어 G_normal 계산
    # ---------------------------
    G_normal = ___

    # ---------------------------
    # TODO 2-3: 각 위치에서의 norm (크기) 계산
    # ---------------------------
    albedo_normal = ___

    threshold = 1e-7
    # ---------------------------
    # TODO 2-4: norm이 너무 작은 경우 threshold로 나눠서 unit normal 벡터 만들기
    # ---------------------------
    G_normal = ___

    # There may be NaN values due to a division by zero
    normals = np.nan_to_num(G_normal)
    return albedo, normals


def project_impl(K, Rt, points):
    """
    Project 3D points into a calibrated camera.
    Input:
        K -- camera intrinsics calibration matrix
        Rt -- 3 x 4 camera extrinsics calibration matrix
        points -- height x width x 3 array of 3D points
    Output:
        projections -- height x width x 2 array of 2D projections
    """
    # Create projection matrix
    # ---------------------------
    # TODO 5-1: 투영 행렬 P = K [R|t] 계산
    # ---------------------------
    projection_Matrix = ___

    # Switch from 3D coordinates to homogeneous coordinates
    extra_ones = np.tile([1], points.shape[0]*points.shape[1])
    extra_ones = extra_ones.reshape((points.shape[0], points.shape[1],1))
    h_points = np.concatenate((points, extra_ones), axis=2)

    # ---------------------------
    # TODO 5-2: 동차좌표계에서 카메라로 투영 (x = P X_h)
    # ---------------------------
    xs  = ___

    # Normalize to convert back from homogeneous coordinates to 2D coordinates
    deno = xs[:,:,2][:,:,np.newaxis]

    # ---------------------------
    # TODO 5-3: z로 나눠서 (u, v) 좌표로 정규화
    # ---------------------------
    normalized_xs = ___

    return normalized_xs[:,:,:2]


def get_pixel_values(img, i, j, u, v, isGrayscale):
    """
    Helper function to return the pixel values based on the position of the window
    """
    if i+u < 0 or i+u >= img.shape[0] or j+v < 0 or j+v >= img.shape[1]:
        return 0 if isGrayscale else np.zeros(img.shape[2])
    return img[i+u][j+v]


def preprocess_ncc_impl(image, ncc_size):
    """
    Prepare normalized patch vectors according to normalized cross
    correlation.

    This is a preprocessing step for the NCC pipeline.  It is expected that
    'preprocess_ncc' is called on every input image to preprocess the NCC
    vectors and then 'compute_ncc' is called to compute the dot product
    between these vectors in two images.

    NCC preprocessing has two steps.
    (1) Compute and subtract the mean.
    (2) Normalize the vector.

    The mean is per channel.  i.e. For an RGB image, over the ncc_size**2
    patch, compute the R, G, and B means separately.  The normalization
    is over all channels.  i.e. For an RGB image, after subtracting out the
    RGB mean, compute the norm over the entire (ncc_size**2 * channels)
    vector and divide.

    If the norm of the vector is < 1e-6, then set the entire vector for that
    patch to zero.

    Patches that extend past the boundary of the input image at all should be
    considered zero.  Their entire vector should be set to 0.

    Patches are to be flattened into vectors with the default numpy row
    major order.  For example, given the following
    2 (height) x 2 (width) x 2 (channels) patch, here is how the output
    vector should be arranged.

    channel1         channel2
    +------+------+  +------+------+ height
    | x111 | x121 |  | x112 | x122 |  |
    +------+------+  +------+------+  |
    | x211 | x221 |  | x212 | x222 |  |
    +------+------+  +------+------+  v
    width ------->

    v = [ x111, x121, x211, x221, x112, x122, x212, x222 ]

    see order argument in np.reshape

    Input:
        image -- height x width x channels image of type float32
        ncc_size -- integer width and height of NCC patch region; assumed to be odd
    Output:
        normalized -- heigth x width x (channels * ncc_size**2) array
    """
    num_channels = image.shape[-1]
    normalized = np.zeros((image.shape[0], image.shape[1], num_channels * ncc_size**2), dtype = np.float32)
    mid_kernel = ncc_size//2
    height, width, channel = image.shape

    for i in range(mid_kernel, height - mid_kernel):
        for j in range(mid_kernel, width - mid_kernel):
            windows = []
            for u in range(channel):
                window = image[i - mid_kernel : i + mid_kernel + 1,
                               j - mid_kernel : j + mid_kernel + 1, u]

                # ---------------------------
                # TODO 3-1: 채널별 평균을 빼고, 벡터로 펼치기
                # ---------------------------
                window = ___

                windows.append(window.T)

            flatten = np.array(windows).flatten()

            # ---------------------------
            # TODO 3-2: flatten 벡터의 L2 norm 계산
            # ---------------------------
            norm = ___

            # ---------------------------
            # TODO 3-3: norm >= 1e-6 이면 정규화, 아니면 0 벡터
            # ---------------------------
            flatten = ___

            normalized[i,j] = flatten
    return normalized


def compute_ncc_impl(image1, image2):
    """
    Compute normalized cross correlation between two images that already have
    normalized vectors computed for each pixel with preprocess_ncc.

    Input:
        image1 -- height x width x (channels * ncc_size**2) array
        image2 -- height x width x (channels * ncc_size**2) array
    Output:
        ncc -- height x width normalized cross correlation between image1 and
               image2.
    """
    # ---------------------------
    # TODO 3-4: 채널/피처 차원(axis=2) 방향으로 내적 합산
    # ---------------------------
    ncc = ___

    return ncc
