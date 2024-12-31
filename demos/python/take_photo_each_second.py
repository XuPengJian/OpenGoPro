import subprocess
import os
import time

# for i in range(10):
#     operation = f'gopro-photo --output {i}.jpg --wired'
#     subprocess.run(operation, shell=True)


import asyncio
from open_gopro import WirelessGoPro, Params, WiredGoPro


# 有线连接gopro
async def main():
    # 执行连拍脚本
    start_time = time.time()
    operation = f'gopro-photo --wired'
    subprocess.run(operation, shell=True)
    end_time = time.time()
    print(f"拍照运行时间：{end_time - start_time}秒")
    async with WiredGoPro() as gopro:
        # 设置基本属性（这个属性我已经在相机里设置好了）
        # await gopro.ble_setting.resolution.set(Params.Resolution.RES_4K)
        # await gopro.ble_setting.fps.set(Params.FPS.FPS_30)
        # await gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        # await asyncio.sleep(2) # Record for 2 seconds
        # await gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)

        # Download all of the files from the camera
        # 下载所拍摄的文件
        media_list = (await gopro.http_command.get_media_list()).data.files
        print(gopro.http_command.get_media_list())
        print(media_list)
        new_medioa = media_list[-1]

        # 遍历所有的文件
        for item in media_list:
            os.makedirs(os.path.dirname(f'download/{item.filename}'), exist_ok=True)
            await gopro.http_command.download_file(camera_file=item.filename, local_file=f'download/{item.filename}')

        # 格式化sd卡
        await gopro.http_command.delete_all()

# 有线连接代码
# async def main():
#     async with WiredGoPro() as gopro:
#         print("gopro是否打开：", gopro.is_open)
#         print("Yay! I'm connected via USB, opened, and ready to send / get data now!")
# gopro = WiredGoPro()
# await gopro.open()
# print("Yay! I'm connected via USB, opened, and ready to send / get data now!")


if __name__ == '__main__':
    asyncio.run(main())
