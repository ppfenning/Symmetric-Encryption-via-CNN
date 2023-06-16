import deeplake
ds = deeplake.load("hub://activeloop/vctk")

if __name__ == '__main__':
    dataloader = ds.tensorflow()