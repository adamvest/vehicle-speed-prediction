import os


class Parameters():
	def __init__(self):
		self.n_processors = 8

		#frame setup
		self.seq_len = 5
		self.overlap = 4
		self.check_interval = 1
		self.use_optical_flow = True
		self.use_both = False
		self.use_three_frames = False
		frames = 3 if self.use_three_frames else 2

		#preprocessing
		self.resize_mode = "crop" # "crop", "rescale", or None
		self.img_w = 600  # 608
		self.img_h = 380  # 184
		self.img_means = [(-0.25843116, -0.21177726, -0.16270572),
			(0.24156884, 0.28822274, 0.33729428)]
		self.img_stds = (1, 1, 1)
		self.minus_point_5 = True

		#data info path
		input = "images"

		if self.use_both:
			input = "both"
		elif self.use_optical_flow:
			input = "flow"

		self.train_data_info_path = "./datainfo/train_df_%d_%d_%d_%s.pickle" \
			% (self.seq_len, self.overlap, frames, input)
		self.valid_data_info_path = "./datainfo/valid_df_%d_%d_%d_%s.pickle" \
			% (self.seq_len, self.overlap, frames, input)
		self.test_data_info_path = "./datainfo/test_df_%d_%d_%d_%s.pickle" \
			% (self.seq_len, self.overlap, frames, input)

		#model
		self.model = "resnet3d" #deepvo
		self.resnet_depth = 34 # 18
		self.linear_size = 2048
		self.rnn_hidden_size = 1000
		self.conv_dropout = (0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.5)
		self.rnn_dropout_out = 0.5
		self.rnn_dropout_between = 0.5
		self.clip = None
		self.batch_norm = True

		#number of channels
		mult = frames if self.model == "deepvo" else 1

		if self.use_both:
			self.num_channels = 5 * mult
		elif self.use_optical_flow:
			self.num_channels = 2 * mult
		else:
			self.num_channels = 3 * mult

		#training
		self.batch_updates = False
		self.epochs = 10
		self.batch_size = 2
		self.pin_mem = True
		self.optim = {"opt": "Adagrad", "lr": 0.0005} # {"opt": "Adam"}

		#load weights
		self.load_weights = True
		self.load_base_deepvo = False
		self.load_conv_only = False
		self.load_model_path = "./models/resnet3d_34_scratch_5_4_2_flow.model.train_0"

		#testing
		self.evaluate_val = True

		#save paths
		base = "scratch"

		if self.load_weights:
			if self.load_base_deepvo:
				base = "base"
			else:
				base = "speeds"

		model = self.model if self.model == "deepvo" else self.model + "_%d" % self.resnet_depth

		self.save_model_path = "./models/%s_%s_%d_%d_%d_%s.model" \
			% (model, base, self.seq_len, self.overlap, frames, input)

		if not os.path.isdir(os.path.dirname(self.save_model_path)):
			os.makedirs(os.path.dirname(self.save_model_path))
		if not os.path.isdir(os.path.dirname(self.train_data_info_path)):
			os.makedirs(os.path.dirname(self.train_data_info_path))


par = Parameters()
