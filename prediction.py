import os
from utils import mask_ada
import argparse
import numpy as np
from MaskPLAN import MASKPLAN

## Global Para ##

list_len = 10
type_dimen = 10
loc_dimen = 20
ada_dimen = 2
area_dimen = 32
room_dimen = 20
sqe_len = 10
code = 25
code_dimen = 64
room_order = [2, 3, 5, 6, 4, 7, 1]  # order when implement post-process

# color tag for each room type, just for visualization
T_list = [[255, 255, 255, 255], [255, 255, 0, 255], [255, 0, 255, 255], [0, 255, 255, 255],
          [0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255], [127, 127, 255, 255], [127, 255, 127, 255]]

## Load Data ##

frontD = np.load('Processed_data/RPLAN_frontdoor.npy')  # vec
bound = np.load('Processed_data/RPLAN_B.npy')  # visual tokens
Testset_ids = np.load('Processed_data/Test_set.npy')  # ids
Testset_ids[0] = 0
bound_domain = np.load('Processed_data/Boundary_BoundingBox.npy')  # vec
bound_domain[0] = [16, 16, 112, 112]


## args ##

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', default='Large', type=str, help='Tiny, Base, Large')
    parser.add_argument('--test_cases', default=1000, type=int)  # test layouts
    parser.add_argument('--par_T', default=0.25, type=float)  # partial input Type
    parser.add_argument('--par_L', default=0., type=float)  # partial input Location
    parser.add_argument('--par_A', default=0.25, type=float)  # partial input Adjacency
    parser.add_argument('--par_S', default=0.25, type=float)  # partial input Size
    parser.add_argument('--par_R', default=0.25, type=float)  # partial input Region
    parser.add_argument('--skip_idx', default=1, type=int,
                        help='which token to skip, default skip first [start] token')

    return parser.parse_args()


## main inference ##

def main(args):
    skip_idx = args.skip_idx
    os.makedirs('Inference/%s_Single_vec/iteration/raw' % (args.model), exist_ok=True)
    os.makedirs('Inference/%s_Single_vec/iteration/post' % (args.model), exist_ok=True)

    ## define model

    dimen_L = 2
    dimen_R = 4

    if args.model == 'Tiny':

        embed_dim = 600
        latent_dim = 2048
        num_heads = 8
        enc_layers = 1
        dec_layers = 1

    elif args.model == 'Base':

        embed_dim = 800
        latent_dim = 3072
        num_heads = 16
        enc_layers = 1
        dec_layers = 1

    elif args.model == 'Large':

        embed_dim = 1000
        latent_dim = 4096
        num_heads = 24
        enc_layers = 1
        dec_layers = 1

    # load MaskPLAN_dir

    MaskPLAN = MASKPLAN(embed_dim, latent_dim, num_heads, enc_layers, dec_layers)
    MaskPLAN.load_weights('MaskPLAN_Trained/All_%s_Single_vec/All' % (args.model))

    # load data

    Input_data = np.load('Processed_data/RPLAN_input_vec.npz')
    file_index = Input_data.files

    T_in = Input_data[file_index[0]]
    L_in = Input_data[file_index[1]]
    A_in = Input_data[file_index[2]]
    S_in = Input_data[file_index[3]]
    R_in = Input_data[file_index[4]]

    class MaskPLAN_Inference():

        def __init__(self):
            super().__init__()

            self.M_T = np.zeros((1, list_len))
            self.M_L = np.zeros((1, list_len, dimen_L))
            self.M_A = np.zeros((1, list_len, list_len - 2))
            self.M_S = np.zeros((1, list_len))
            self.M_R = np.zeros((1, list_len, dimen_R))

            self.In_T = np.zeros((1, list_len))
            self.In_L = np.zeros((1, list_len, dimen_L))
            self.In_A = np.zeros((1, list_len, list_len - 2))
            self.In_S = np.zeros((1, list_len))
            self.In_R = np.zeros((1, list_len, dimen_R))

        def reset(self, site_id):

            self.bound = bound[site_id].reshape((1, 25))
            self.fd = frontD[site_id].reshape((1, 2))

            self.M_T[0, :skip_idx] = T_in[site_id, :skip_idx]
            self.M_L[0, :skip_idx, :] = L_in[site_id, :skip_idx, :]
            self.M_A[0, :skip_idx, :] = A_in[site_id, :skip_idx, :]
            self.M_S[0, :skip_idx] = S_in[site_id, :skip_idx]
            self.M_R[0, :skip_idx, :] = R_in[site_id, :skip_idx, :]

            self.In_T[0, :skip_idx] = T_in[site_id, :skip_idx]
            self.In_L[0, :skip_idx, :] = L_in[site_id, :skip_idx, :]
            self.In_A[0, :skip_idx, :] = A_in[site_id, :skip_idx, :]
            self.In_S[0, :skip_idx] = S_in[site_id, :skip_idx]
            self.In_R[0, :skip_idx, :] = R_in[site_id, :skip_idx, :]

            self.M_T[0, skip_idx:] = 0
            self.M_L[0, skip_idx:] = 0
            self.M_A[0, skip_idx:] = 0
            self.M_S[0, skip_idx:] = 0
            self.M_R[0, skip_idx:] = 0

            self.In_T[0, skip_idx:] = 0
            self.In_L[0, skip_idx:] = 0
            self.In_A[0, skip_idx:] = 0
            self.In_S[0, skip_idx:] = 0
            self.In_R[0, skip_idx:] = 0

        def partial_input(self, site_id):

            valid = (T_in[site_id] == type_dimen - 2).argmax(axis=0) - 1

            partial_T = np.random.choice(valid - 1, round(valid * args.par_T), replace=False) + 1
            self.M_T[0, partial_T] = T_in[site_id, partial_T]
            self.In_T[0, partial_T] = T_in[site_id, partial_T]

            partial_L = np.random.choice(valid - 1, round(valid * args.par_L), replace=False) + 1
            self.M_L[0, partial_L] = L_in[site_id, partial_L]
            self.In_L[0, partial_L] = L_in[site_id, partial_L]
            print(L_in[site_id, partial_L])

            partial_S = np.random.choice(valid - 1, round(valid * args.par_S), replace=False) + 1
            self.M_S[0, partial_S] = S_in[site_id, partial_S]
            self.In_S[0, partial_S] = S_in[site_id, partial_S]

            partial_R = np.random.choice(valid - 1, round(valid * args.par_R), replace=False) + 1
            self.M_R[0, partial_R] = R_in[site_id, partial_R]
            self.In_R[0, partial_R] = R_in[site_id, partial_R]

            partial_A = mask_ada(np.random.choice(valid, round(valid * args.par_A), replace=False), list_len,
                                 A_in[site_id])
            self.M_A[0] = partial_A
            self.In_A[0] = partial_A

        def inference_interation(self, site_id):

            # get boudnary

            # boundary_pt = np.array([[0, 0], [0, 479], [639, 479], [639, 0]]) # Square bounding box
            # if boundary_pt.ndim == 1:
            #     boundary_pt = [[0, 0], [0, 127], [127, 127], [127, 0]]
            # boundary_pt = [[16, 16], [16, 122], [122, 122], [122, 16]]

            # Inference, skip all [start] token and defined token

            for k in range(int(list_len * 5 - 1)):

                if 0 <= k < list_len - 1:  # Type

                    if self.In_T[0, k + 1] != 0:
                        continue
                    else:
                        pred = MaskPLAN.predict(
                            [self.M_T, self.M_L, self.M_A, self.M_S, self.M_R, self.bound, self.fd, self.In_T,
                             self.In_L, self.In_A, self.In_S, self.In_R])[0]
                        self.In_T[0, k + 1] = np.array(np.argmax(pred[0, k, :]))
                        if self.In_T[0, k + 1] == type_dimen - 2: num_room = k

                elif list_len - 1 + 1 <= k < list_len * 2 - 1:  # Ada

                    pred = MaskPLAN.predict(
                        [self.M_T, self.M_L, self.M_A, self.M_S, self.M_R, self.bound, self.fd, self.In_T, self.In_L,
                         self.In_A, self.In_S, self.In_R])[1]
                    self.In_A[0, k - list_len + 1] = np.array(np.argmax(pred[0, k - list_len, :, :], axis=-1))

                elif list_len * 2 - 1 + 1 <= k < list_len * 3 - 1:  # Loc

                    if (self.In_L[0, k - list_len * 2 + 1] != np.zeros(2)).any():
                        continue
                    else:
                        pred = MaskPLAN.predict(
                            [self.M_T, self.M_L, self.M_A, self.M_S, self.M_R, self.bound, self.fd, self.In_T,
                             self.In_L, self.In_A, self.In_S, self.In_R])[2]
                        self.In_L[0, k - list_len * 2 + 1] = np.array(
                            np.argmax(pred[0, k - list_len * 2, :, :], axis=-1))

                elif list_len * 3 - 1 + 1 <= k < list_len * 4 - 1:  # Size

                    if self.In_S[0, k - list_len * 3 + 1] != 0:
                        continue
                    else:
                        pred = MaskPLAN.predict(
                            [self.M_T, self.M_L, self.M_A, self.M_S, self.M_R, self.bound, self.fd, self.In_T,
                             self.In_L, self.In_A, self.In_S, self.In_R])[3]
                        self.In_S[0, k - list_len * 3 + 1] = np.array(np.argmax(pred[0, k - list_len * 3, :]))

                elif list_len * 4 - 1 + 1 <= k:  # Region

                    if (self.In_R[0, k - list_len * 4 + 1] != np.zeros(4)).any():
                        continue
                    else:
                        pred = MaskPLAN.predict(
                            [self.M_T, self.M_L, self.M_A, self.M_S, self.M_R, self.bound, self.fd, self.In_T,
                             self.In_L, self.In_A, self.In_S, self.In_R])[4]
                        self.In_R[0, k - list_len * 4 + 1] = np.array(
                            np.argmax(pred[0, k - list_len * 4, :, :], axis=-1))

            # Generate imgs

            # predict raw

            corners = self.In_R[0, 1:num_room + 1]
            x_min = ((corners[:, 0] + 1) / loc_dimen) * (bound_domain[site_id, 3] - bound_domain[site_id, 1]) + \
                    bound_domain[site_id, 1]
            y_min = ((corners[:, 1] + 1) / loc_dimen) * (bound_domain[site_id, 2] - bound_domain[site_id, 0]) + \
                    bound_domain[site_id, 0]
            x_max = ((corners[:, 2] + 1) / loc_dimen) * (bound_domain[site_id, 3] - bound_domain[site_id, 1]) + \
                    bound_domain[site_id, 1]
            y_max = ((corners[:, 3] + 1) / loc_dimen) * (bound_domain[site_id, 2] - bound_domain[site_id, 0]) + \
                    bound_domain[site_id, 0]

            print("Done")
            return x_min, y_min, x_max, y_max

    return MaskPLAN_Inference()


if __name__ == "__main__":

    # init
    args = parse_args()

    # run
    model = main(args)

    for num, site in enumerate(Testset_ids[:args.test_cases]):
        model.reset(site)
        model.partial_input(site)
        print(model.inference_interation(site))
        if num % 100 == 0: print(num)

