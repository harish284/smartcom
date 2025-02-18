from collections import deque
from typing import List

def floodFillBFS(image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:
    # Get the original color at the starting cell
    oldColor = image[sr][sc]
    
    # If the old color is already the new color, no changes are needed
    if oldColor == newColor:
        return image
    
    rows, cols = len(image), len(image[0])
    
    # Queue for BFS
    queue = deque()
    queue.append((sr, sc))
    
    # Update the color of the starting cell
    image[sr][sc] = new
    
    # Directions for up, down, left, right
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while queue:
        x, y = queue.popleft()
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check boundaries and color match
            if 0 <= nx < rows and 0 <= ny < cols and image[nx][ny] == oldColor:
                # Fill with the new color
                image[nx][ny] = newColor
                queue.append((nx, ny))
    
    return image

# ---------------------- SAMPLE USAGE ----------------------
if __name__ == "__main__":
    # Sample Input
    image = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1]
    ]
    sr, sc = 1, 1  # Starting row and column
    newColor = 2   # The color we want to fill with

    # Call the BFS Flood Fill function
    result = floodFillBFS(image, sr, sc, newColor)

    # Print the updated image
    print("Updated Image After Flood Fill (BFS):")
    for row in result:
        print(row)
