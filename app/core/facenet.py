import tensorflow as tf
from app.core.config import config
import numpy as np

class FaceNetModel:
    def __init__(self):
        self.model = tf.Graph()
        with self.model.as_default():
            graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(config.pre_trained_model, 'rb') as f:
                graph_def.ParseFromString(f.read())
                tf.import_graph_def(graph_def, name='')

    def get_embeddings(self, image):
        with tf.compat.v1.Session(graph=self.model) as sess:
            input_set = sess.graph.get_tensor_by_name('input:0')
            embeddings = sess.graph.get_tensor_by_name('embeddings:0')
            phase_train = sess.graph.get_tensor_by_name('phase_train:0')

            image = tf.image.resize(image, (160, 160))
            image = tf.image.per_image_standardization(image)
            image = tf.expand_dims(image, 0)

            feed_dict = {input_set: image.eval(session = sess), phase_train: False}
            emb = sess.run(embeddings, feed_dict=feed_dict)
            return emb

facenet_model = FaceNetModel()