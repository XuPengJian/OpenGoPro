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
    # 预计照片数量
    second_num = int(end_time - start_time)
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
        new_media = media_list[-1]

        # 遍历所有的文件
        # for item in media_list:
        #     os.makedirs(os.path.dirname(f'download/{item.filename}'), exist_ok=True)
        #     await gopro.http_command.download_file(camera_file=item.filename, local_file=f'download/{item.filename}')
        download_start_time = time.time()

        # Gopro的文件命名规则，每999张就会创建新的文件夹
        max_value = 999
        full_parts = second_num // max_value
        remaining_value = second_num % max_value

        # 每一个文件夹的文件数量列表
        parts = [max_value] * full_parts + [remaining_value]

        for i, item in enumerate(media_list):
            for j in range(parts[i]):
                file_name = str(item.filename).split('/')[0] + '/' + str(item.filename).split('/')[-1][:4] + \
                            str(int(str(item.filename).split('/')[-1][4:8]) + j) + '.JPG'
                os.makedirs(os.path.dirname(f'download'), exist_ok=True)
                try:
                    await gopro.http_command.download_file(camera_file=file_name, local_file=f'download/{file_name.split("/")[-1]}')
                except Exception as e:
                    print(e)
        download_end_time = time.time()
        print('---------------------------------------')
        # 执行完毕
        print(f"拍照运行时间:{end_time - start_time}秒")
        print(f'预计图片数量{second_num}')
        print('照片下载完成')
        print(f'照片下载时间:{download_end_time - download_start_time}秒')
        # 格式化sd卡
        await gopro.http_command.delete_all()
        print('已经格式化sd卡')
        print('---------------------------------------')


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
