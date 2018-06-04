"""Methods to load images from the sprites repository."""
import os, glob


def get_all_image_filenames(game: str='smb1') -> list:
    """
    Get the filenames for all images of a given game.

    Args:
        game: a string indicating the game to get sprites for. should be
            either `smb1` or `smb2`

    Returns:
        a list of the filenames of images in the game sprite directory

    """
    # check that the game directory is valid
    if game != 'smb1' and game != 'smb2':
        error = "`game` must be either 'smb1' or 'smb2', but is {}"
        raise ValueError(error.format(repr(game)))
    # the directory containing this module
    module_dir = os.path.dirname(os.path.abspath(__file__))
    # create a pattern for finding files recursively with a glob
    pattern = '{}/{}/**/*.*'.format(module_dir, game)
    # return the resulting list of the recursive glob search
    return glob.glob(pattern, recursive=True)


def extract_image_class(filename: str) -> str:
    """
    Extract the class label for a given filename.

    Args:
        filename: the filename to extract a class label for

    Returns:
        a class label based on the image's filename

    """
    # extract the filename itself without the absolute path
    filename = filename.split('/')[-1]
    # remove any unique descriptive text following a dash
    filename = filename.split('-')[0]
    # remove any spaces for simplicity
    filename = filename.replace(' ', '')
    # replace file-type information with nothing
    filename = filename.replace('.gif', '').replace('.png', '')

    return filename


image_filenames = get_all_image_filenames()
image_classes = [extract_image_class(filename) for filename in image_filenames]
