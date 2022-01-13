from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import subprocess as sp
import open3d as o3d
import pandas as pd
import numpy as np
import copy as cp
import math
import time
import os

from tkinter import *
from tkinter import ttk
import threading

def Scan(filename, stop_number=1000, stop_mode=1):
    #-> Run the slam and produce the map
    os.chdir("/app/build/")
    command = f"./Demarrage /dpds/ORB_SLAM3/Vocabulary/ORBvoc.txt /dpds/ORB_SLAM3/Examples/Monocular/RealSense_D435i.yaml {str(stop_number)} {stop_mode} {filename}"
    print(command)
    try:
        sp.run(command, shell=True, check=True)
    except Exception:
        print("Scan failed !")
    else:
        print("Scan succeeded")

def Load(filename):
    if filename.find(".csv") == -1: filename = filename + ".csv"
    filename = "/app/datasets/maps/" + filename
    return o3d.io.read_point_cloud(filename, format="xyz")

# def AlphaShapes(pcd, alpha=0.035):
#     print(f"alpha={alpha:.3f}")
#     mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
#     mesh.compute_vertex_normals()
#     o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

# def BallPivoting(pcd):
#     pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
#     pcd.estimate_normals()
#     pcd.orient_normals_consistent_tangent_plane(100)
#     radii = [0.05, 0.05, 0.1, 0.04]
#     rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
#         pcd, o3d.utility.DoubleVector(radii))
#     o3d.visualization.draw_geometries([pcd, rec_mesh])

# def PoissonEstimation(pcd):
#     pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
#     pcd.estimate_normals()
#     pcd.orient_normals_consistent_tangent_plane(100)

#     with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
#         mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)

#     densities = np.asarray(densities)
#     density_colors = plt.get_cmap('plasma')((densities - densities.min()) / (densities.max() - densities.min()))
#     density_colors = density_colors[:, :3]
#     density_mesh = o3d.geometry.TriangleMesh()
#     density_mesh.vertices = mesh.vertices
#     density_mesh.triangles = mesh.triangles
#     density_mesh.triangle_normals = mesh.triangle_normals
#     density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
#     o3d.visualization.draw_geometries([density_mesh])

# def display_inlier_outlier(cloud, ind):
#     inlier_cloud = cloud.select_by_index(ind)
#     outlier_cloud = cloud.select_by_index(ind, invert=True)

#     print("Showing outliers (red) and inliers (gray): ")
#     outlier_cloud.paint_uniform_color([1, 0, 0])
#     inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
#     o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

def MenuModif(map):
    global end, retour
    end = False
    retour = 0

    root = Tk()
    root.geometry("350x350")
    root.title("Geometry modification")
    tab_control = ttk.Notebook(root)

    tabOR = ttk.Frame(tab_control)    
    tab_control.add(tabOR, text="Outlier Removing")
    Label(tabOR, text="STATISTICAL").grid(row=0)
    Label(tabOR, text="neighbors").grid(row=1)
    Label(tabOR, text="standard dev.").grid(row=2)
    e1 = Entry(tabOR)
    e2 = Entry(tabOR)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)

    def ApplyORS():
        global end, retour
        neighbors = int(e1.get())
        std = float(e2.get())
        retour = map.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=std)[0]
        end = True
    
    btn1 = Button(tabOR, text ="Apply", command = ApplyORS)
    btn1.grid(row=0, column=1)

    Label(tabOR, text="RADIAL").grid(row=3)
    Label(tabOR, text="neighbors").grid(row=4)
    Label(tabOR, text="radius").grid(row=5)
    e3 = Entry(tabOR)
    e4 = Entry(tabOR)
    e3.grid(row=4, column=1)
    e4.grid(row=5, column=1)

    def ApplyORR():
        global end, retour
        neighbors = int(e3.get())
        rad = float(e4.get())
        retour = map.remove_radius_outlier(nb_points=neighbors, radius=rad)[0]
        end = True
    
    btn2 = Button(tabOR, text ="Apply", command = ApplyORR)
    btn2.grid(row=3, column=1)


    tabSurf = ttk.Frame(tab_control)   
    tab_control.add(tabSurf, text="Surface Reconstruction")
    Label(tabSurf, text="ALPHA SHAPES").grid(row=0)
    Label(tabSurf, text="alpha").grid(row=1)
    e5 = Entry(tabSurf)
    e5.grid(row=1, column=1)

    def ApplyALPHA():
        global end, retour
        alpha = float(e5.get())
        retour = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(map, alpha)
        end = True
    
    btn3 = Button(tabSurf, text ="Apply", command = ApplyALPHA)
    btn3.grid(row=0, column=1)

    Label(tabSurf, text="VOXELS").grid(row=2)
    Label(tabSurf, text="voxel size").grid(row=3)
    e6 = Entry(tabSurf)
    e6.grid(row=3, column=1)

    def ApplyVOX():
        global end, retour
        size = float(e6.get())
        retour = o3d.geometry.VoxelGrid.create_from_point_cloud(map, voxel_size=0.04)
        end = True
    
    btn4 = Button(tabSurf, text ="Apply", command = ApplyVOX)
    btn4.grid(row=2, column=1)

    Label(tabSurf, text="POISSON").grid(row=4)
    Label(tabSurf, text="depth").grid(row=5)
    e7 = Entry(tabSurf)
    e7.grid(row=5, column=1)

    def ApplyPOIS():
        global end, retour
        depth = int(e7.get())
        map.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
        map.estimate_normals()
        map.orient_normals_consistent_tangent_plane(100)

        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(map, depth=depth)

        densities = np.asarray(densities)
        density_colors = plt.get_cmap('plasma')((densities - densities.min()) / (densities.max() - densities.min()))
        density_colors = density_colors[:, :3]
        density_mesh = o3d.geometry.TriangleMesh()
        density_mesh.vertices = mesh.vertices
        density_mesh.triangles = mesh.triangles
        density_mesh.triangle_normals = mesh.triangle_normals
        density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
        retour = density_mesh
        end = True

    btn5 = Button(tabSurf, text ="Apply", command = ApplyPOIS)
    btn5.grid(row=4, column=1)

    tab_control.pack(expand=1, fill='both')
    while (not end):
        time.sleep(1/60)
        root.update()
    root.destroy()
    end = False
    return retour

def Menu():
    global end
    end = False
    main = Tk()
    main.title("Main menu")
    main.geometry("500x350")

    Label(main, text="LAUNCH vSLAM").grid(row=0, column=1)
    Label(main, text="Stop at").grid(row=1)
    selected = IntVar()
    rad1 = Radiobutton(main,text='Frame', value="1", variable=selected).grid(row=1, column=1)
    rad2 = Radiobutton(main,text='Time          ', value="0", variable=selected).grid(row=1, column=2)
    fnS = Entry(main, width=7)
    fnS.insert(END, '400')
    fnS.grid(row=1, column=4)
    Label(main, text="File name    ").grid(row=3)
    fnE = Entry(main)
    fnE.insert(END, 'map')
    fnE.grid(row=3, column=1)

    def Launch():
        global end
        stopVal = int(fnS.get())
        filename = fnE.get()
        Scan(filename, stopVal, selected)
        end = True
    
    SLAMbtn = Button(main, text ="Launch", command = Launch)
    SLAMbtn.grid(row=3, column=2)

    Label(main, text="LOAD POINT CLOUD").grid(row=5, column=1)
    Label(main, text="File name").grid(row=6)
    
    OptionList = os.listdir("/app/datasets/maps")
    variable = StringVar(main)
    variable.set(OptionList[0])
    opt = OptionMenu(main, variable, *OptionList)
    opt.grid(row=6, column=1)
    opt.config(width=15, font=('Helvetica', 10))

    def LoadPC():
        global end
        filename = str(variable)
        print(variable)
        main.destroy()
        Visual(filename)
        end = True
    
    SLAMbtn = Button(main, text ="Load", command = LoadPC)
    SLAMbtn.grid(row=6, column=2)

    while (not end):
        time.sleep(1/60)
        main.update()
    end = False
    main.destroy()

def Visual(filename):
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name="Visualizer")
    geo = Load(filename)
    geometries = []
    geometries.append(geo)

    def capture_depth(vis):
        depth = vis.capture_depth_float_buffer()
        plt.imshow(np.asarray(depth))
        plt.show()
        return False

    def capture_image(vis):
        image = vis.capture_screen_float_buffer()
        plt.imshow(np.asarray(image))
        plt.show()
        return False

    def rollPlus(vis):
        z = math.radians(5)
        angles = np.array([[0, 0, z]]).T
        r = geometries[0].get_rotation_matrix_from_axis_angle(angles)
        geometries[0].rotate(r)
        return False

    def rollMinus(vis):
        z = -math.radians(5)
        angles = np.array([[0, 0, z]]).T
        r = geometries[0].get_rotation_matrix_from_axis_angle(angles)
        geometries[0].rotate(r)
        return False

    def yawPlus(vis):
        y = math.radians(5)
        angles = np.array([[0, y, 0]]).T
        r = geometries[0].get_rotation_matrix_from_axis_angle(angles)
        geometries[0].rotate(r)
        return False

    def yawMinus(vis):
        y = -math.radians(5)
        angles = np.array([[0, y, 0]]).T
        r = geometries[0].get_rotation_matrix_from_axis_angle(angles)
        geometries[0].rotate(r)
        return False

    def pitchPlus(vis):
        x = math.radians(5)
        angles = np.array([[x, 0, 0]]).T
        r = geometries[0].get_rotation_matrix_from_axis_angle(angles)
        geometries[0].rotate(r)
        return False

    def pitchMinus(vis):
        x = -math.radians(5)
        angles = np.array([[x, 0, 0]]).T
        r = geometries[0].get_rotation_matrix_from_axis_angle(angles)
        geometries[0].rotate(r)
        return False

    def MapChange(vis):
        try:
            geometries.append(MenuModif(geometries[0]))
            vis.add_geometry(geometries[-1], False)
            vis.remove_geometry(geometries[0], False)
            geometries.pop(0)
        except Exception: 
            pass       

    def Reset(vis):
        for g in geometries:
            vis.remove_geometry(g)
        geometries = [geo]
        vis.add_geometry(geo)

    vis.register_key_callback(69, yawPlus)
    vis.register_key_callback(81, yawMinus)
    vis.register_key_callback(87, pitchPlus)
    vis.register_key_callback(83, pitchMinus)
    vis.register_key_callback(65, rollPlus)
    vis.register_key_callback(68, rollMinus)
    vis.register_key_callback(ord("."), MapChange)
    vis.register_key_callback(ord("\n"), Reset)
    for g in geometries:
        vis.add_geometry(g)
        
    stay_open = True
    while(stay_open):
        for g in geometries:
            vis.update_geometry(g)
        stay_open = vis.poll_events()
        vis.update_renderer()
        time.sleep(1/60)

    vis.destroy_window()

if __name__ == "__main__":
    # Scan("pi", 1100, 1)
    Visual("sashimi")
    # Menu()
