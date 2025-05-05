import io
import os
import tifffile
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from imageAnalyzer.settings import BASE_DIR

class FilterImage:
    def __init__(self, savepath, image, red_band, green_band, blue_band, suffix):
        self.savepath = savepath
        self.suffix = suffix
        self.image = tifffile.imread(io.BytesIO(image.read()) ) # shape: (bands, rows, cols)
        self.num_bands = self.image.shape[0]
        self.wavelengths = np.linspace(400, 2500, self.num_bands)

        # Stretch RGB channels and put them into a 2d array
        red = self.stretch_contrast(self.image[red_band])
        green = self.stretch_contrast(self.image[green_band])
        blue = self.stretch_contrast(self.image[blue_band])
        self.rgb = np.stack([red, green, blue], axis=-1)

        self.red_band = red_band
        self.green_band = green_band
        self.blue_band = blue_band

        self.row, self.col = red.shape

    def stretch_contrast(self, band, low=2, high=98):
        p_low, p_high = np.percentile(band, (low, high))
        return np.clip((band - p_low) / (p_high - p_low + 1e-8), 0, 1)


    def run(self):
        # ----- Save false RGB image -----
        save_rgb_to = os.path.join(self.savepath, f"false_rgb_{self.suffix}.png")

        plt.figure(figsize=(6, 6))
        plt.imshow(self.rgb)
        plt.title(f"False Color RGB\nR: {self.wavelengths[self.red_band]:.1f}nm, "
                f"G: {self.wavelengths[self.green_band]:.1f}nm, "
                f"B: {self.wavelengths[self.blue_band]:.1f}nm")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_rgb_to, dpi=300)
        plt.close()
        print("Saved RGB to:", save_rgb_to)

        # ----- Extract RGB channels -----
        r = self.rgb[:, :, 0]
        g = self.rgb[:, :, 1]
        b = self.rgb[:, :, 2]

        # Mask: Red bright, Green & Blue dark (e.g., vegetation or water-like)
        # Create an empty boolean array for the mask, same shape as a single band
        mask = np.zeros_like(r, dtype=bool)

        # Get the image dimensions
        rows, cols = r.shape

        # Loop over every pixel in the image
        for i in range(rows):
            for j in range(cols):
                red_val = r[i, j]
                green_val = g[i, j]
                blue_val = b[i, j]

                if red_val > 0.6 and green_val < 0.4 and blue_val < 0.4:
                    mask[i, j] = True

        print(f"{np.count_nonzero(mask)} pixels selected for spectral averaging.")

        # ----- Extract and average spectra -----
        selected_spectra = self.image[:, mask]  # shape: (bands, num_selected_pixels)
        avg_spectrum = selected_spectra.mean(axis=1)

        # Find spectral peak
        peak_idx = np.argmax(avg_spectrum)
        peak_wavelength = self.wavelengths[peak_idx]
        peak_val = avg_spectrum[peak_idx]

        # ----- Plot the spectral signature -----
        save_signature_to = os.path.join(self.savepath, f"spectral_signature_{self.suffix}.png")

        plt.figure(figsize=(8, 4))
        plt.plot(self.wavelengths, avg_spectrum, color='red')
        plt.axvline(x=peak_wavelength, color='gray', linestyle='--', alpha=0.5)
        plt.text(peak_wavelength + 10, peak_val * 0.95,
                f'Peak: {peak_wavelength:.1f} nm',
                fontsize=9, color='black')
        plt.title("Average Spectral Signature of Selected Pixels")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Radiance / Intensity")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_signature_to, dpi=300)
        plt.close()
        print("Saved spectral signature to:", save_signature_to)

        # ----- Optionally return output paths -----
        return save_rgb_to, save_signature_to
