import unittest
from map_objects.rectangle import Rect

class TestRectangleCreate(unittest.TestCase):

    def test_create_rect(self):
        # Given
        rect = Rect(2, 3, 4, 5)

        # Then
        self.assertEqual(rect.x1, 2)
        self.assertEqual(rect.y1, 3)
        self.assertEqual(rect.x2, 6)
        self.assertEqual(rect.y2, 8)

    def test_create_rect_2(self):
        # Given
        rect = Rect(0, 0, 5, 5)

        # Then
        self.assertEqual(rect.x1, 0)
        self.assertEqual(rect.x2, 5)
        self.assertEqual(rect.y1, 0)
        self.assertEqual(rect.y2, 5)

class TestRectangleCenter(unittest.TestCase):

    def test_even_sides(self):
        # Given
        rect = Rect(0, 0, 4, 4)

        # When
        x, y = rect.center()

        # Then
        self.assertEqual(x, 2)
        self.assertEqual(y, 2)

    def test_uneven_sides(self):
        # Given
        rect = Rect(0, 0, 5, 5)

        # When
        x, y = rect.center()

        # Then
        self.assertEqual(x, 2)
        self.assertEqual(y, 2)

    def test_mixed_sides(self):
        # Given
        rect = Rect(0, 0, 4, 7)

        # When
        x, y = rect.center()

        # Then
        self.assertEqual(x, 2)
        self.assertEqual(y, 3)

    def test_not_in_corner(self):
        # Given
        rect = Rect(2, 3, 4, 5)

        # When
        x, y = rect.center()

        # Then
        self.assertEqual(x, 4)
        self.assertEqual(y, 5)

class TestRectangleIntersects(unittest.TestCase):

    def test_intersects_lower_right(self):
        # Given
        rect_a = Rect(0, 0, 5, 5)
        rect_b = Rect(2, 2, 5, 5)

        # When
        result = rect_a.intersects(rect_b)

        # Then
        self.assertTrue(result)

    def test_intersects_lower_left(self):
        # Given
        rect_a = Rect(2, 0, 5, 5)
        rect_b = Rect(0, 2, 5, 5)

        # When
        result = rect_a.intersects(rect_b)

        # Then
        self.assertTrue(result)

    def test_intersects_upper_right(self):
        # Given
        rect_a = Rect(0, 2, 5, 5)
        rect_b = Rect(2, 0, 5, 5)

        # When
        result = rect_a.intersects(rect_b)
        
        # Then
        self.assertTrue(result)

    def test_intersects_upper_left(self):
        # Given
        rect_a = Rect(2, 2, 5, 5)
        rect_b = Rect(0, 0, 5, 5)

        # When
        result = rect_a.intersects(rect_b)

        # Then
        self.assertTrue(result)

    def test_intersects_aligned_horizontally(self):
        # Given
        rect_a = Rect(2, 2, 5, 5)
        rect_b = Rect(1, 2, 5, 5)

        # When
        result = rect_a.intersects(rect_b)

        # Then
        self.assertTrue(result)

    def test_intersects_aligned_vertically(self):
        # Given
        rect_a = Rect(2, 2, 5, 5)
        rect_b = Rect(2, 1, 5, 5)

        # When
        result = rect_a.intersects(rect_b)

        # Then
        self.assertTrue(result)
    
    def test_intersects_touching_horizontally(self):
        # Given
        rect_a = Rect(0, 0, 5, 5)
        rect_b = Rect(5, 0, 5, 5)

        # When
        result = rect_a.intersects(rect_b)
        
        # Then
        self.assertTrue(result)

    def test_intersects_tounching_vertically(self):
        # Given
        rect_a = Rect(0, 0, 5, 5)
        rect_b = Rect(0, 5, 5, 5)

        # When
        result = rect_a.intersects(rect_b)

        # Then
        self.assertTrue(result)

    def test_intersects_touching_corner(self):
        # Given
        rect_a = Rect(0, 0, 5, 5)
        rect_b = Rect(5, 5, 5, 5)

        # When
        result = rect_a.intersects(rect_b)

        # Then
        self.assertTrue(result)

    def test_no_intersection(self):
        # Given
        rect_a = Rect(0, 0, 4, 4)
        rect_b = Rect(5, 5, 4, 4)

        # When
        result = rect_a.intersects(rect_b)
        
        # Then
        self.assertFalse(result)
