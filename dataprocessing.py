import numpy as np
import scipy.signal as sig
from scipy.fft import fft, ifft
import wave
import soundfile as sf
import matplotlib.pyplot as plt


def ampSig(fname):
    str_data, params = read_wavefile(fname)
    nchannels, sampwidth, framerate, nframes = params[:4]
    wave_data = np.fromstring(str_data, dtype=np.short)

    #plt.plot(wave_data)
    return wave_data







def resave(fname, start, end, newfname):
    y, sr = sf.read(file=fname, dtype='int16')
    out = y[start:end]
    sf.write(file=newfname, data=out, samplerate=sr,subtype='PCM_16')
dict_init = ['games', 'downloads', 'distributives', 'projects', 'documents', 'photos', 'music', 'films', 'books']
dict_new = ['games', 'downloads', 'distributives', 'projects', 'documents', 'photos', 'music', 'films', 'books']


def read_wavefile(sound_path):
    recordData = wave.open(sound_path)
    params = recordData.getparams()
    nframes = params[3]
    str_data = recordData.readframes(nframes)
    recordData.close()

    return [str_data, params]


def nothing_silence():
    for element in zip(dict_init, dict_new):
        initName = "C:\\Users\\mishu\\Downloads\\Лаба 2 АА\\Лаба 2 АА\\Lab_2\\voise_recording\\{init}.wav".format(init=element[0])
        newfname = "C:\\Users\\mishu\\Downloads\\Лаба 2 АА\\Лаба 2 АА\\Lab_2\\new\\{out}".format(out=element[1])
        i = 0
        id = 0
        str_data, params = read_wavefile(initName)
        nchannels, sampwidth, framerate, nframes = params[:4]
        wave_data = np.fromstring(str_data, dtype=np.short)

        waveVAD = VAD(wave_data, sr=framerate, frame_time=0.02, frame_shift=0.5, noise_frame_end=0, eTh=5000)
        data = []
        for _ in range(10):
            outfile = "{el}{name}.wav".format(el=newfname, name=id)
            id += 1
            resave(initName, waveVAD[1][i], waveVAD[1][i + 1], outfile)
            i += 2
            w = wave.open(outfile, 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
        finishfile = "C:\\Users\\mishu\\Downloads\\Лаба 2 АА\\Лаба 2 АА\\Lab_2\\new\\{el}.wav".format(el=element[1])
        output = wave.open(finishfile, 'wb')
        output.setparams(data[0][0])
        k = 0
        for k in range(len(data)):
            output.writeframes(data[k][1])
        output.close()










def cleaning(y, sr, frame_time, frame_shift):
    frameWidth, frameShift, frameCount, df = frame_size(y, sr, frame_time, frame_shift)
    y_without = np.zeros_like(y)
    noise = y[: frameWidth]
    for i in range(int(round(y.size / frameWidth)) - 1):
        alf = 1.35
        beta = 0.0
        yi = y[i*frameWidth: (i + 1)*frameWidth]
        spectr_sig = fft(yi)
        arg = np.angle(spectr_sig)
        spectr_noise = fft(noise[: yi.size])
        delt = np.abs(spectr_sig) - alf * np.abs(spectr_noise)
        tet = beta * np.abs(spectr_noise)
        spectr_res = np.where(delt > 0, delt, tet)
        y_without[i * frameWidth: i * frameWidth + yi.size] = ifft(spectr_res * np.exp(1j * arg))
    return y_without



def filtering(y, sr, wsr):
    b, a = sig.butter(4, wsr, 'low', output='ba', fs=sr, analog=False)
    return sig.filtfilt(b, a, y)


def combine(y, sr, wsr):
    y = cleaning(y)
    return filtering(y, sr, 800)


def frame_size(data, sr, frame_time, frame_shift):
    frameWidth = int(round(frame_time * sr))
    frameShift = int(frame_shift * frameWidth)
    df = frameWidth - frameShift
    frameCount = int(round(data.size / df)) - 1
    return frameWidth, frameShift, frameCount, df


def dataToEnergy(data, sr, frame_time, frame_shift):
    frameWidth, frameShift, frameCount, df = frame_size(data, sr, frame_time, frame_shift)
    data = data.astype(float)
    E = np.array(
        [np.sum(data[df * i: df * i + frameWidth] ** 2) / frameWidth for i in range(frameCount)]
    )
    return np.array(E)


def VAD(data, sr, frame_time, frame_shift, noise_frame_end=0, eTh=2000):
    frameWidth, frameShift, frameCount, df = frame_size(data, sr, frame_time, frame_shift)
    E = dataToEnergy(data, sr, frame_time, frame_shift)
    if noise_frame_end > 0:
        e_Th = np.max(E[: noise_frame_end])
        print('Нижняя граница шума: ', e_Th)
        e_Th = e_Th * 5
    else:
        e_Th = eTh
    st_j_counter = False
    dj_len = 0
    tickData = []
    vadData = np.where(E <= e_Th, 0, 1)
    for j in range(1, frameCount):
        if vadData[j - 1] < vadData[j]:
            st_j_counter = False
            if j - dj_len >= 0:
                tickData.append((j - dj_len) * df)
            else:
                tickData.append(0)
        elif vadData[j - 1] > vadData[j]:
            st_j_counter, dj = True, 0
            tickData.append(j * df)
        else:
            if st_j_counter:
                dj += 1
                if dj == dj_len:
                    tickData.append(j * df)
                    st_j_counter, dj = False, 0
        if j == frameCount - 1 and st_j_counter and dj > 0:
            tickData.append(j * df)
    return vadData, tickData


def find_voice_activity(vad):
    for i in range(1, vad.shape[0] - 35):
        if vad[i - 1] == 0 and vad[i]:
            if np.sum(vad[i: i + 35]) < 33:
                vad[i] = 0
    return vad


def segmentation(data, sr, frame_time, frame_shift, voice_active, Zpor=70):
    Z_ = np.where(data >= 0, 1, 0)
    frameWidth, frameShift, frameCount, df = frame_size(data, sr, frame_time, frame_shift)
    # energy = dataToEnergy(data, sr, frame_time, frame_shift)
    Z = []
    for i in range(frameCount):
        Zi = Z_[i * df: i * df + frameWidth].astype(float)
        Z2 = Zi[1:]
        Z1 = Zi[:-1]
        Z.append(np.sum(np.abs(Z2 - Z1)) / 2)
    Z = np.array(Z)[voice_active]
    indexes = []
    for i in range(1, Z.shape[0] - 1):
        if Z[i] < Zpor < Z[i + 1] or Z[i] > Zpor > Z[i + 1]:
            indexes.append(i)
    return indexes
