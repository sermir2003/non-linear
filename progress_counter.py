import time

bleaching_line = '\r' + ' ' * 60 + '\r'


class ProgressCounter:
    def __init__(self, action_name):
        self.action_name = action_name
        print('{} has begun'.format(action_name))
        print('Progress: 0%', end='')
        self.enable = True
        self.start_time = time.time()

    def update_progress(self, progress):
        cur_time = time.time()
        delta = cur_time - self.start_time
        time_left = delta / progress * (1 - progress)
        print(bleaching_line + 'Progress: {:.1f}%; time left: {:.2f}s; time used: {:.2f}s'.format(100 * progress,
                                                                                                  time_left, delta),
              end='')

    def finish_action(self):
        self.enable = False
        cur_time = time.time()
        delta = cur_time - self.start_time
        print(bleaching_line + 'Progress: 100%; time used: {:.2f}s'.format(delta))

    def __del__(self):
        if self.enable:
            self.finish_action()
