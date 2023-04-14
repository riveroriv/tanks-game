import numpy as np

def transform(t_matrix, vertices):
    vert_list = [[v[0], v[1], 1] for v in vertices]
    vert_matrix = np.transpose(np.array(vert_list))
    # 2. Aplicar la matriz de transformacion
    new_matrix = np.dot(t_matrix, vert_matrix)
    # 3. Convertir nuevos vertices al formato [(x, y), ...]
    new_matrix2 = np.transpose(new_matrix)
    new_vertices = [(nv[0], nv[1]) for nv in new_matrix2]
    # 4. Reasignar nuevos vertices
    return new_vertices

def rotate(theta, vertices, center=None):
    vert_array = np.array(vertices)
    if center == None :
        x , y = np.sum(vert_array, axis=0) / vert_array.shape[0]
    else :
        x, y = center
    # M1
    to_origin_trf = np.array([
        [1, 0, -x],
        [0, 1, -y],
        [0, 0, 1]
    ])
    # M2
    rotation_trf = np.array([
        [np.cos(np.radians(theta)), -np.sin(np.radians(theta)), 0],
        [np.sin(np.radians(theta)), np.cos(np.radians(theta)), 0],
        [0, 0, 1]
    ])
    # M3
    from_origin_trf = np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
    ])
    return transform(np.dot(from_origin_trf, np.dot(rotation_trf, to_origin_trf)), vert_array)