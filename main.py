import aiohttp
import asyncio
from typing import List
import re

        
async def fetch_matrix(url: str) -> List[List[int]]:
    """
    Asynchronously fetches the matrix from the given URL.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Raise an exception for bad status codes
                text = await response.text()
                lines = text.strip().split('\n')
                # Filter out non-numeric lines
                numeric_lines = [line for line in lines if not line.startswith('+') and not line.endswith('+')]
                cleaned_lines = [re.sub(r'[^a-zA-Z0-9\s]', '', line) for line in numeric_lines]
                matrix = [list(map(int, line.split())) for line in cleaned_lines]
                return matrix
        except aiohttp.ClientResponseError as e:
            raise Exception(f"Failed to fetch matrix: HTTP {e.status}")
        except aiohttp.ClientConnectionError as e:
            raise Exception(f"Connection error: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

def spiral_traversal(matrix: List[List[int]]) -> List[int]:
    # Your existing spiral traversal function remains the same
    result = []
    n = len(matrix)
    top, bottom, left, right = 0, n - 1, 0, n - 1

    while top <= bottom and left <= right:
        # Traverse from left to right
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1

        # Traverse from top to bottom
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1

        # Traverse from right to left
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1

        # Traverse from bottom to top
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

    return result

async def get_matrix(url: str) -> List[int]:
    """
    Fetches the matrix from the given URL and returns its spiral traversal.
    """
    matrix = await fetch_matrix(url)
    if not matrix or not all(len(row) == len(matrix) for row in matrix):
        raise Exception("The fetched data is not a square matrix")
    return spiral_traversal(matrix)

# Example usage
async def test_get_matrix():
    url = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
    try:
        result = await get_matrix(url)
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(test_get_matrix())

