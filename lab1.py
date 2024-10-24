import soundfile as sf
import dataprocessing as dp
import scipy.signal as sig
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
dictionary = ['Y']

# dictionary = [
#     'books', 'films', 'music', 'photos', 'documents',
#    'projects', 'distributives', 'downloads', 'games'
# ]
#
# naming = {
#     'books': 'Книги', 'films': 'фильмы', 'music': 'музыка',
#     'photos': 'Фотографии', 'documents': 'документы', 'projects': 'проекты',
#     'distributives': 'дистрибутивы', 'downloads': 'загрузки', 'games': 'игры',
# }

wave_data_two = dp.ampSig("C:\\Users\\mishu\\Downloads\\Лаба 2 АА\\Лаба 2 АА\\Lab_2\\new\\books1.wav")
plt.subplot(511)
plt.plot(wave_data_two[0:2500])
plt.title('|-----к-----|')

plt.subplot(512)
plt.plot(wave_data_two[2500:4000])
plt.title('|-----н-----|')

plt.subplot(513)
plt.plot(wave_data_two[4000:6000])
plt.title('|-----и-----|')

plt.subplot(514)
plt.plot(wave_data_two[6000:8000])
plt.title('|-----г-----|')

plt.subplot(515)
plt.plot(wave_data_two[8000:])
plt.title('|-----и-----|')
plt.tight_layout(pad=1)
plt.show()

wave_data_three = dp.ampSig("C:\\Users\\mishu\\Downloads\\Лаба 2 АА\\Лаба 2 АА\\Lab_2\\new\\music1.wav")

plt.subplot(611)
plt.plot(wave_data_three[0:2000])
plt.title('|-----м-----|')

plt.subplot(612)
plt.plot(wave_data_three[2000:4500])
plt.title('|-----у-----|')
plt.subplot(613)
plt.plot(wave_data_three[4500:6000])
plt.title('|-----з-----|')

plt.subplot(614)
plt.plot(wave_data_three[6000:8500])
plt.title('|-----ы-----|')

plt.subplot(615)
plt.plot(wave_data_three[8500:10000])
plt.title('|-----к-----|')

plt.subplot(616)
plt.plot(wave_data_three[10000:12000])
plt.title('|-----а-----|')

plt.tight_layout(pad=0.5)
plt.show()









# signal_cleaning = True
# #dp.nothing_silence()
# frame_time = 0.02
# frame_shift = 0.5
# path_to_folder = 'C:\\Users\\mishu\\Downloads\\Лаба 2 АА\\Лаба 2 АА\\Lab_2\\voise_recording'
# for w_ind in range(len(dictionary)):
#     filename = dictionary[w_ind]
#     file_name = f'{path_to_folder}\\{filename}.wav'
#     print(file_name)
#     y, sr = sf.read(file=file_name, dtype='int16')
#     frameWidth, frameShift, frameCount, df = dp.frame_size(y, sr, frame_time, frame_shift)
#
#     enData = dp.dataToEnergy(y, sr=sr,
#                              frame_time=frame_time,
#                              frame_shift=frame_shift)
#     vadData, tickData = dp.VAD(y, sr=sr, frame_time=frame_time,
#                                frame_shift=frame_shift, noise_frame_end=0, eTh=25000)
#     vadData1 = vadData.copy()
#     for i in range(vadData1.size - 10):
#         if vadData1[i] == 1 and vadData1[i + 1] == 0:
#             if np.sum(vadData1[i: i + 10]) > 1:
#                 vadData1[i: i + 10] = 1
#     vadData1 = dp.find_voice_activity(vadData1)
#     dt = []
#     if len(tickData):
#         for j in range(int(len(tickData) / 2) - 1):
#             dt.append(tickData[j * 2 + 2] - tickData[j * 2 + 1])
#         min_pause = 10 * frameWidth
#         tickData2 = list(tickData[0: 1])
#         for j in range(int(len(tickData) / 2) - 1):
#             pause = tickData[j * 2 + 2] - tickData[j * 2 + 1]
#             if pause > min_pause:
#                 tickData2.append(tickData[2 * j + 1])
#                 tickData2.append(tickData[2 * j + 2])
#         tickData2.append(tickData[len(tickData) - 1])
#     if not signal_cleaning:
#         fig, ax = plt.subplots(3, 1, figsize=(12, 9))
#         ax[0].set_title(naming[dictionary[w_ind]])
#         plt.subplots_adjust(hspace=0.35)
#         ax[0].plot(np.arange(y.size) / df, y)
#         ax[1].plot(enData)
#         ax[2].plot(vadData1)
#         fig, ax = plt.subplots(2, 1, figsize=(5, 3))
#         ax[0].plot(enData[vadData1.astype(bool)])
#         ax[0].set_title(naming[dictionary[w_ind]])
#         ind = dp.segmentation(y, sr, frame_time, frame_shift, vadData1.astype(bool))
#         print(ind)
#         [ax[1].axvline(x) for x in ind]
#         plt.show()
#         if input() == 's':
#             break
#
# if signal_cleaning:
#     fig, ax = plt.subplots(3, 1, figsize=(8, 6))
#     plt.subplots_adjust(hspace=0.45)
#     y_n_mvc = dp.cleaning(y, sr, frame_time, frame_shift)
#     sf.write(f'{path_to_folder}\\cleaned_SP.wav', y_n_mvc, sr)
#     y_n_filter = dp.filtering(y, sr, 900)
#     sf.write(f'{path_to_folder}\\cleaned_filter.wav', y_n_filter, sr)
#     # y_combine = dp.combine(y, sr, 800)
#     # sf.write(f'{path_to_folder}\\cleaned_combine.wav', y_combine, sr)
#     ax[0].plot(y_n_mvc)
#     ax[0].set_title('сигнал после МВС')
#     ax[1].plot(y_n_filter)
#     ax[1].set_title('Сигнал после прохождения фильтра')
#     ax[2].plot(y)
#     ax[2].set_title('Исходный сигнал')
#     plt.show()
#     SPM = sig.welch(y, fs=sr, nperseg=480, noverlap=240, detrend=None, scaling='density')
#     SPM_MVC = sig.welch(y_n_mvc, fs=sr, nperseg=480, noverlap=240, detrend=None, scaling='density')
#     SPM_FILTER = sig.welch(y_n_filter, fs=sr, nperseg=480, noverlap=240, detrend=None, scaling='density')
#     _, ax = plt.subplots(3, 1, figsize=(8, 6))
#     plt.subplots_adjust(hspace=0.45)
#     ax[0].plot(*SPM)
#     ax[0].set_title('СПМ первоначального сигнала')
#     ax[1].plot(*SPM_MVC)
#     ax[1].set_title('СПМ сигнала очищенного МВС')
#     ax[2].plot(*SPM_FILTER)
#     ax[2].set_title('СПМ сигнала очищенного фильтром')
#     plt.show()
