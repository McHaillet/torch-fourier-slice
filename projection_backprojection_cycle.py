"""A simple projection/backprojection cycle implementation."""
import mrcfile
import torch
from scipy.stats import special_ortho_group

from torch_fourier_slice import project_3d_to_2d, backproject_2d_to_3d


N_IMAGES = 250
torch.manual_seed(42)

# load a volume and normalise
volume = torch.tensor(mrcfile.read('/Users/burta2/data/4v6x_bin4.mrc'))
volume -= torch.mean(volume)
volume /= torch.std(volume)

# rotation matrices for projection (operate on xyz column vectors)
rotations = torch.tensor(
    special_ortho_group.rvs(dim=3, size=N_IMAGES, random_state=42)
).float()

# make projections
projections = project_3d_to_2d(
    volume,
    rotation_matrices=rotations,
    pad=True,
    pixel_spacing_angstroms=4,
    maximum_resolution_angstroms=None,
)  # (b, h, w)

# reconstruct volume from projections
reconstruction = backproject_2d_to_3d(
    images=projections,
    rotation_matrices=rotations,
    pad=True,
    pixel_spacing_angstroms=4,
    maximum_resolution_angstroms=None,
)
# reconstruction -= torch.mean(reconstruction)
# reconstruction = reconstruction / torch.std(reconstruction)

# fsc
# _reconstructionfsc = fsc(, volume)
# print(_fsc)

# visualise
# import napari
#
# viewer = napari.Viewer()
# viewer.add_image(projections.numpy(), name='projections')
#
# viewer = napari.Viewer(ndisplay=3)
# viewer.add_image(volume.numpy(), name='ground truth')
# viewer.add_image(reconstruction.numpy(), name='reconstruction')
# napari.run()
