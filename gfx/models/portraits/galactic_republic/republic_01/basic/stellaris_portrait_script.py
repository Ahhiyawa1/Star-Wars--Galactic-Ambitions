import cv2
import numpy as np

def align_clothing(input_path, reference_path, output_path):
    # Load images
    input_img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    reference_img = cv2.imread(reference_path, cv2.IMREAD_UNCHANGED)

    # Resize reference image to match input dimensions
    ref_height, ref_width = input_img.shape[:2]
    reference_resized = cv2.resize(reference_img, (ref_width, ref_height), interpolation=cv2.INTER_LINEAR)

    # Convert to grayscale
    input_gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    reference_gray = cv2.cvtColor(reference_resized, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection for precise outline
    input_edges = cv2.Canny(input_gray, 50, 150)
    reference_edges = cv2.Canny(reference_gray, 50, 150)

    # Find contours
    input_contours, _ = cv2.findContours(input_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    reference_contours, _ = cv2.findContours(reference_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if input_contours and reference_contours:
        # Get largest contours
        input_contour = max(input_contours, key=cv2.contourArea)
        reference_contour = max(reference_contours, key=cv2.contourArea)
        
        # Find convex hulls for better shape fitting
        input_hull = cv2.convexHull(input_contour)
        reference_hull = cv2.convexHull(reference_contour)
        
        # Extract keypoints
        input_pts = np.float32(input_hull[:, 0, :])
        reference_pts = np.float32(reference_hull[:, 0, :])
        
        # Ensure both have the same number of points
        if len(input_pts) > len(reference_pts):
            input_pts = input_pts[:len(reference_pts)]
        else:
            reference_pts = reference_pts[:len(input_pts)]
        
        # Estimate transformation matrix
        matrix, _ = cv2.estimateAffinePartial2D(reference_pts, input_pts)
        
        # Warp the reference image
        warped_reference = cv2.warpAffine(reference_resized, matrix, (ref_width, ref_height))
        
        # Save the result
        cv2.imwrite(output_path, warped_reference)
        print(f"Transformed image saved to {output_path}")
    else:
        print("Error: Could not find contours for precise matching.")


# Example usage
if __name__ == "__main__":
    align_clothing(
        input_path="input.png",
        reference_path="reference.png",
        output_path="output_warped.png"
    )
