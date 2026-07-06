import unittest

from fcfa_detector import FCFADetector


class DetectorTests(unittest.TestCase):
    def test_synthetic_prediction(self) -> None:
        detector = FCFADetector()
        X, y = detector.build_dataset(samples_per_class=8)
        detector.train(X, y)

        sample_image = detector._make_bill_image("5000")
        prediction = detector.predict_image(sample_image)

        self.assertIn(prediction, detector.denominations)


if __name__ == "__main__":
    unittest.main()
