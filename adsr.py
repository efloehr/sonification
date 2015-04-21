class ADSR(object):
    def __init__(self, attack_ms, decay_ms, sustain_level, release_ms, samples_per_second):
        self.attack_ms = attack_ms
        self.decay_ms = decay_ms
        self.sustain_level = sustain_level
        self.release_ms = release_ms
        self.samples_per_second = samples_per_second
        self.samples_per_ms = samples_per_second / 1000.0
        self.attack_samples = int(round(attack_ms * self.samples_per_ms))
        self.decay_samples = int(round(decay_ms * self.samples_per_ms))
        self.release_samples = int(round(release_ms * self.samples_per_ms))

    def envelope(self, total_ms):
        sustain_ms = max(0, total_ms - self.attack_ms - self.decay_ms - self.release_ms)
        for level in self.attack_levels():
            yield level
        for level in self.decay_levels():
            yield level
        for level in self.sustain_levels(sustain_ms):
            yield level
        for level in self.release_levels():
            yield level
            
    def attack_levels(self):
        add_incr = 1.0 / self.attack_samples
        current_level = 0
        for level in xrange(self.attack_samples):
            current_level += add_incr
            yield current_level
    
    def decay_levels(self):
        sub_incr = (1.0 - self.sustain_level) / self.decay_samples
        current_level = 1.0
        for level in xrange(self.decay_samples):
            current_level -= sub_incr
            yield current_level
    
    def sustain_levels(self, sustain_ms):
        for level in xrange(int(round(self.samples_per_ms * sustain_ms))):
            yield self.sustain_level
    
    def release_levels(self):
        sub_incr = self.sustain_level / self.release_samples
        current_level = self.sustain_level
        for level in xrange(self.release_samples):
            current_level -= sub_incr
            yield current_level
