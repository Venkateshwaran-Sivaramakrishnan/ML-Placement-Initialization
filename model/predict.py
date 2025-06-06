import numpy as np
import os
import time
import tensorflow as tf
tf.compat.v1.enable_eager_execution()
import numpy as np
from tensorflow.keras.models import load_model
import json
import cv2
from Inference.decode_function import *
from utils import mask_ada
import argparse
from shapely.geometry import Polygon,MultiPolygon,LinearRing,MultiPoint,LineString
from shapely.ops import unary_union

from MaskPLAN_BaseAll_vec import *

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
room_order = [2,3,5,6,4,7,1] # order when implement post-process

# color tag for each room type, just for visualization
T_list = [[255,255,255,255],[255,255,0,255],[255,0,255,255],[0,255,255,255],
          [0,0,255,255],[255,0,0,255],[0,255,0,255],[127,127,255,255],[127,255,127,255]]

def parse_args():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output_file")
    parser.add_argument("--boundary_file", default="model/RPLAN_B.npy", help="Path to the boundary")
    parser.add_argument('--model', default='Large', type=str, help='Tiny, Base, Large')
    parser.add_argument('--test_cases', default=1000, type=int) # test layouts
    parser.add_argument('--par_T', default=0.25, type=float) # partial input Type
    parser.add_argument('--par_L', default=0.25, type=float) # partial input Location
    parser.add_argument('--par_A', default=0.25, type=float) # partial input Adjacency 
    parser.add_argument('--par_S', default=0.25, type=float) # partial input Size 
    parser.add_argument('--par_R', default=0.25, type=float) # partial input Region 
    parser.add_argument('--skip_idx', default=1, type=int,
                        help='which token to skip, default skip first [start] token')
    parser.add_argument('--gpu', default=0, type=int, help="GPU to run this inference on")
    
    return parser.parse_args()

def infer(args, cluster_tensor_data, count, bound, frontD, bound_domain):

    skip_idx = args.skip_idx
    os.makedirs('Inference/%s_Single_vec/iteration/raw' % (args.model),exist_ok=True)
    os.makedirs('Inference/%s_Single_vec/iteration/post' % (args.model),exist_ok=True)

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

    # load MaskPLAN

    MaskPLAN = MASKPLAN(embed_dim,latent_dim,num_heads,enc_layers,dec_layers)
    MaskPLAN.load_weights('MaskPLAN_Trained/All_%s_Single_vec/All' % (args.model))

    # load data

    T_in = np.array([entry["T"] for entry in cluster_tensor_data])
    L_in = np.zeros((count, 10, 2))
    A_in = np.array([entry["A"] for entry in cluster_tensor_data])
    S_in = np.array([entry["S"] for entry in cluster_tensor_data])
    R_in = np.zeros((count, 10, 4))

    class MaskPLAN_Inference():
            
        def __init__(self):
            super().__init__()

            self.M_T = np.zeros((1,list_len))
            self.M_L = np.zeros((1,list_len,dimen_L))
            self.M_A = np.zeros((1,list_len,list_len-2))
            self.M_S = np.zeros((1,list_len))
            self.M_R = np.zeros((1,list_len,dimen_R))

            self.In_T = np.zeros((1,list_len))
            self.In_L = np.zeros((1,list_len,dimen_L))
            self.In_A = np.zeros((1,list_len,list_len-2))
            self.In_S = np.zeros((1,list_len))
            self.In_R = np.zeros((1,list_len,dimen_R))

        def reset(self,site_id):

            self.bound = bound[site_id].reshape((1,25))
            self.fd = frontD[site_id] .reshape((1,2))

            self.M_T[0,:skip_idx] = T_in[site_id,:skip_idx]
            self.M_L[0,:skip_idx,:] = L_in[site_id,:skip_idx,:]
            self.M_A[0,:skip_idx,:] = A_in[site_id,:skip_idx,:]
            self.M_S[0,:skip_idx] = S_in[site_id,:skip_idx]
            self.M_R[0,:skip_idx,:] = R_in[site_id,:skip_idx,:]

            self.In_T[0,:skip_idx] = T_in[site_id,:skip_idx]
            self.In_L[0,:skip_idx,:] = L_in[site_id,:skip_idx,:]
            self.In_A[0,:skip_idx,:] = A_in[site_id,:skip_idx,:]
            self.In_S[0,:skip_idx] = S_in[site_id,:skip_idx]
            self.In_R[0,:skip_idx,:] = R_in[site_id,:skip_idx,:]

            self.M_T[0,skip_idx:] = 0
            self.M_L[0,skip_idx:] = 0
            self.M_A[0,skip_idx:] = 0
            self.M_S[0,skip_idx:] = 0
            self.M_R[0,skip_idx:] = 0

            self.In_T[0,skip_idx:] = 0
            self.In_L[0,skip_idx:] = 0
            self.In_A[0,skip_idx:] = 0
            self.In_S[0,skip_idx:] = 0
            self.In_R[0,skip_idx:] = 0

        def partial_input(self,site_id):

            valid = (T_in[site_id]==type_dimen-2).argmax(axis=0)-1

            # partial_T = np.random.choice(valid-1, round(valid*args.par_T), replace=False) + 1
            partial_T = [i+1 for i in range(valid+1)]
            self.M_T[0,partial_T] = T_in[site_id,partial_T]
            self.In_T[0,partial_T] = T_in[site_id,partial_T]

            partial_L = np.random.choice(valid-1, round(valid*args.par_L), replace=False) + 1
            self.M_L[0,partial_L] = L_in[site_id,partial_L]
            self.In_L[0,partial_L] = L_in[site_id,partial_L]

            partial_S = np.random.choice(valid-1, round(valid*args.par_S), replace=False) + 1
            self.M_S[0,partial_S] = S_in[site_id,partial_S]
            self.In_S[0,partial_S] = S_in[site_id,partial_S]

            partial_R = np.random.choice(valid-1, round(valid*args.par_R), replace=False) + 1
            self.M_R[0,partial_R] = R_in[site_id,partial_R]
            self.In_R[0,partial_R] = R_in[site_id,partial_R]

            partial_A = mask_ada(np.random.choice(valid, round(valid*args.par_A), replace=False),list_len,A_in[site_id])
            self.M_A[0] = partial_A
            self.In_A[0] = partial_A

        def inference_interation(self,site_id):

            # get boudnary

            pts = []
            types = []
            unioned_rooms = None

            #boundary = cv2.imread('test1.png',cv2.IMREAD_UNCHANGED)[:,:,-1]
            #boundary[np.where(boundary>100)] = 255
            #boundary_pt = get_bound_pt(boundary)
            #if boundary_pt.ndim == 1:
            #    boundary_pt = [[0,0],[0,127],[127,127],[127,0]]
            boundary_pt = [[0,0],[0,127],[127,127],[127,0]]
            boundary_line = LinearRing(boundary_pt)
            #boundary_outside = Polygon([[0,0],[0,127],[127,127],[127,0]]).difference(Polygon(boundary_line))

            # fill boundary in img

            #reconstructed = np.zeros((128,128,4))
            #cv2.fillPoly(reconstructed, [np.array(boundary_line.buffer(2).exterior.coords[:-1])[:,np.newaxis,:].astype(np.int32)], color=[255]*4)
            #cv2.fillPoly(reconstructed, [np.array(boundary_line.coords[:-1])[:,np.newaxis,:].astype(np.int32)], color=[0]*4)
            #reconst_post = reconstructed.copy()
        
            # Inference, skip all [start] token and defined token

            for k in range(self.In_T.shape[1]):
                if self.In_T[0, k] == type_dimen - 2:
                    num_room = k
                    break
        
            for k in range(int(list_len*5-1)):

                if 0<= k < list_len-1: # Type

                    if self.In_T[0,k+1] != 0: continue
                    else: 
                        pred = MaskPLAN.predict([self.M_T,self.M_L,self.M_A,self.M_S,self.M_R,self.bound,self.fd,self.In_T,self.In_L,self.In_A,self.In_S,self.In_R])[0]
                        if self.In_T[0,k+1] == type_dimen-2: num_room = k
                        self.In_T[0,k+1] = np.array(np.argmax(pred[0,k, :]))

                elif list_len-1+1<= k < list_len*2-1: # Ada

                    pred = MaskPLAN.predict([self.M_T,self.M_L,self.M_A,self.M_S,self.M_R,self.bound,self.fd,self.In_T,self.In_L,self.In_A,self.In_S,self.In_R])[1]
                    self.In_A[0,k-list_len+1] = np.array(np.argmax(pred[0,k-list_len, :, :],axis=-1))
                
                elif list_len*2-1+1<= k < list_len*3-1: # Loc

                    if (self.In_L[0,k-list_len*2+1] != np.zeros(2)).any(): continue
                    else: 
                        pred = MaskPLAN.predict([self.M_T,self.M_L,self.M_A,self.M_S,self.M_R,self.bound,self.fd,self.In_T,self.In_L,self.In_A,self.In_S,self.In_R])[2]
                        self.In_L[0,k-list_len*2+1] = np.array(np.argmax(pred[0,k-list_len*2, :, :],axis=-1))
                
                elif list_len*3-1+1<= k < list_len*4-1: # Size

                    if self.In_S[0,k-list_len*3+1] != 0: continue
                    else: 
                        pred = MaskPLAN.predict([self.M_T,self.M_L,self.M_A,self.M_S,self.M_R,self.bound,self.fd,self.In_T,self.In_L,self.In_A,self.In_S,self.In_R])[3]
                        self.In_S[0,k-list_len*3+1] = np.array(np.argmax(pred[0,k-list_len*3, :]))
                
                elif list_len*4-1+1<= k: # Region

                    if (self.In_R[0,k-list_len*4+1] != np.zeros(4)).any(): continue
                    else: 
                        pred = MaskPLAN.predict([self.M_T,self.M_L,self.M_A,self.M_S,self.M_R,self.bound,self.fd,self.In_T,self.In_L,self.In_A,self.In_S,self.In_R])[4]
                        self.In_R[0,k-list_len*4+1] = np.array(np.argmax(pred[0,k-list_len*4, :, :],axis=-1))
                        
            # Generate imgs

            # predict raw

            corners=self.In_R[0,1:num_room+1]
            x_min = ((corners[:,0]+1)/loc_dimen)*(bound_domain[site_id,3] - bound_domain[site_id,1]) + bound_domain[site_id,1]
            y_min = ((corners[:,1]+1)/loc_dimen)*(bound_domain[site_id,2] - bound_domain[site_id,0]) + bound_domain[site_id,0]
            x_max = ((corners[:,2]+1)/loc_dimen)*(bound_domain[site_id,3] - bound_domain[site_id,1]) + bound_domain[site_id,1]
            y_max = ((corners[:,3]+1)/loc_dimen)*(bound_domain[site_id,2] - bound_domain[site_id,0]) + bound_domain[site_id,0]
            
            #overlay = reconstructed.copy()  # used for semi-transparent fill
            
            for i in range(num_room-1):
                # Get rectangle coordinates (4 corners)
                line = LineString([[y_min[i], x_min[i]], [y_max[i], x_max[i]]])
                envelope = line.envelope

                if envelope.geom_type == "Polygon":
                    pt = np.array(envelope.exterior.coords[:-1])
                else:
                    # Handle the degenerate case, e.g., repeat the point or create a small box
                    pt = np.array([[envelope.x, envelope.y]] * 4)
                
                # pt = np.array(LineString([[y_min[i], x_min[i]], [y_max[i], x_max[i]]]).envelope.exterior.coords[:-1])
                pts.append(pt)

                # Get fill color from T_list (should be RGB tuple)
                #fill_color = T_list[int(self.In_T[0, i + 1])]  # e.g., (100, 200, 255)
#
                ## Fill room on overlay (not directly on image)
                #cv2.fillPoly(overlay, [pt[:, np.newaxis, :].astype(np.int32)], color=fill_color)
#
                ## Add semi-transparent overlay to original image
                #alpha = 0.6  # transparency factor
                #cv2.addWeighted(overlay, alpha, reconstructed, 1 - alpha, 0, dst=reconstructed)
#
                ## Compute bounding box for label placement
                #x_min_label = pt[:, 0].min()
                #x_max_label = pt[:, 0].max()
                #y_min_label = pt[:, 1].min()
                #y_max_label = pt[:, 1].max()
                #center_x = int((x_min_label + x_max_label) / 2)
                #center_y = int((y_min_label + y_max_label) / 2)
#
                ## Get text size to center it properly
                #label = str(i + 1)
                #font = cv2.FONT_HERSHEY_SIMPLEX
                #font_scale = 0.4
                #thickness = 1
                #text_size = cv2.getTextSize(label, font, font_scale, thickness)[0]
                #text_x = center_x - text_size[0] // 2
                #text_y = center_y + text_size[1] // 2
#
                ## Draw label
                #cv2.putText(reconstructed, label, (text_x, text_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
#
                types.append(self.In_T[0, i + 1])
            #for pt in pts:
            #    cv2.polylines(reconstructed, [pt[:, np.newaxis, :].astype(np.int32)], isClosed=True, color=(0, 0, 0), thickness=1)
            # Number of nodes to consider
            num_nodes = len(cluster_tensor_data[site_id]['node_list'])

            # Extract only the first coordinate from each polygon up to num_nodes
            first_coords = [
                [pts[i][0], pts[i][2]] if i < len(pts) and len(pts[i]) > 2 else [[0, 0], [0, 0]]
                for i in range(num_nodes)
            ]

            # Save to entry
            entry = cluster_tensor_data[site_id]
            entry["coordinates"] = first_coords
        
            #print(cluster_tensor_data[site_id])
            # post-process

            #living = None
#
            #for m in room_order:
            #    
            #        if m in types:
            #            
            #            indexs = np.where(np.array(types)==m)[0].tolist()
#
            #            for n in indexs:
#
            #                if pts[n].ndim>1 and pts[n].shape[0]>2:
#
            #                    coords = pts[n]
#
            #                    if unioned_rooms:
            #                        unioned_lines = []
#
            #                        if unioned_rooms.geom_type == 'MultiPolygon':
            #                            for g in unioned_rooms.geoms:
            #                                unioned_lines.append(g.exterior)
#
            #                        else:
            #                            unioned_lines = [unioned_rooms.exterior]
#
            #                        for t in range(4):
#
            #                            pt1,pt2 = coords[t],coords[(t+1)%4]
            #                            for unioned_line in unioned_lines:
            #                                pt1,pt2 = align_target(pt1,pt2,unioned_line,8)
            #                            pt1,pt2 = align_target(pt1,pt2,boundary_line,16)
#
            #                            coords[t],coords[(t+1)%4] = pt1,pt2
            #                        room = Polygon(coords).envelope.difference(unioned_rooms)
            #                        room = room.difference(boundary_outside)
            #                        if room.geom_type == 'MultiPolygon':
            #                            room = room.geoms[find_max(room.geoms)]
            #                        if room.geom_type == 'GeometryCollection':
            #                            room = room.geoms[0]
            #                        if room.area > 0.1:
#
            #                            if len(unioned_lines) > 1:
            #                                geolis = []
            #                                for l in unioned_rooms.geoms:
            #                                    geolis.append(l)
            #                                geolis.append(room)
            #                                unioned_rooms = unary_union(MultiPolygon(geolis))
            #                            else:
            #                                if unioned_rooms.geom_type == 'MultiPolygon':
            #                                    unioned_rooms = unioned_rooms.geoms[0]
            #                                unioned_rooms = unary_union(MultiPolygon([room,unioned_rooms]))
            #                            
            #                            cv2.fillPoly(reconst_post, [np.array(room.exterior.coords[:-1])[:,np.newaxis,:].astype(np.int32)], T_list[int(types[n])])
            #                            if int(types[n]) == 1: living = room
            #                        
            #                    else:
#
            #                        for t in range(4):
#
            #                            pt1,pt2 = coords[t],coords[(t+1)%4]
            #                            pt1,pt2 = align_target(pt1,pt2,boundary_line,16)
            #                            coords[t],coords[(t+1)%4] = pt1,pt2
#
            #                        unioned_rooms = Polygon(coords).envelope.difference(boundary_outside)
            #                        if unioned_rooms.geom_type == 'MultiPolygon':
            #                            unioned_rooms = unioned_rooms.geoms[find_max(unioned_rooms.geoms)]
            #                        coorners = np.array(unioned_rooms.exterior.coords[:-1])
            #                        if coorners.ndim>1 and coorners.shape[0]>2:
            #                            cv2.fillPoly(reconst_post, [coorners[:,np.newaxis,:].astype(np.int32)], T_list[int(types[n])])
            #                        
            #boundary_poly = Polygon(boundary_line)
            #rest = boundary_poly.difference(unioned_rooms)
            #if rest.geom_type == 'MultiPolygon':
            #    for geo in rest.geoms:
            #        if geo.area > 3:
            #            scaled = geo.buffer(3)
            #            if scaled.intersects(living): cv2.fillPoly(reconst_post, [np.array(geo.exterior.coords[:-1])[:,np.newaxis,:].astype(np.int32)], T_list[1])
            #            else: cv2.fillPoly(reconst_post, [np.array(geo.exterior.coords[:-1])[:,np.newaxis,:].astype(np.int32)], T_list[7])
            #else: 
            #    if rest.area > 3:
            #        scaled = rest.buffer(3)
            #        if scaled.intersects(living): cv2.fillPoly(reconst_post, [np.array(rest.exterior.coords[:-1])[:,np.newaxis,:].astype(np.int32)], T_list[1])
            #        else: cv2.fillPoly(reconst_post, [np.array(rest.exterior.coords[:-1])[:,np.newaxis,:].astype(np.int32)], T_list[7])
#
            #cv2.imwrite('Inference/%s_Single_vec/iteration/raw/%d.png' % (args.model,site_id),reconstructed)
            #cv2.imwrite('Inference/%s_Single_vec/iteration/post/%d.png' % (args.model,site_id),reconst_post)
    
    return MaskPLAN_Inference()

def main():

    # init
    args = parse_args()

    gpus = tf.config.list_physical_devices('GPU')

    if gpus:
        selected = gpus[args.gpu]
        print(f"USING {selected}")
        tf.config.set_visible_devices(selected, 'GPU')

    # Load the npy file (list of dictionaries)
    cluster_tensor_data = np.load(args.input_file, allow_pickle=True)
    bound = np.load(args.boundary_file, allow_pickle=True)

    # Convert to a Python list (optional but recommended for iteration)
    cluster_tensor_data = cluster_tensor_data.tolist()
    cluster_tensor_data_predict = []

    # Example: Print each entry (can be filtered or formatted as needed)
    count = len(cluster_tensor_data)
    Testset_ids = [i for i in range(count)]
    frontD = [np.array([0, 63]) for i in range(count)]
    boundary = np.array(bound[0])
    bound = [boundary for i in range(count)]
    bounded_domain = [0, 0, 127, 127]
    bound_domain = np.array([bounded_domain for i in range(count)])

    for i in range(len(cluster_tensor_data)):
        entry = cluster_tensor_data[i]
        entry["bound"] = boundary
        entry["bound_domain"] = bounded_domain

    # run
    model = infer(args, cluster_tensor_data, count, bound, frontD, bound_domain)

    count = len(cluster_tensor_data)
    print(f"Total: {count}")

    infer_start_time = time.time()

    for num,site in enumerate(Testset_ids[:count]):
            model.reset(site)
            model.partial_input(site)
            model.inference_interation(site)
            print(f"Done: {site}")
    
    infer_end_time = time.time() - infer_start_time
    with open("infer_time.txt", "a") as log_file:
        log_file.write(f"[✓] Inference completed in {infer_end_time:.2f} seconds\n")
    
    np.save(args.output_file, cluster_tensor_data, allow_pickle=True)

if __name__ == "__main__":
    main()
