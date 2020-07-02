import mbuild as mb


class CH2_Bead(mb.Compound):
    def __init__(self, name='CH2_Bead'):
        super(CH2_Bead, self).__init__()

        self.name = name

        bead = mb.Particle(pos=[0.0, 0.0, 0.0], name='_CH2')
        self.add(bead)
        up_port = mb.Port(anchor=bead, orientation=[0, 0, 1], separation=0.05)
        down_port = mb.Port(anchor=bead, orientation=[0, 0, -1], separation=0.05)
        self.add(up_port, label='up')
        self.add(down_port, label='down')


class CH3_Bead(mb.Compound):
    def __init__(self, name='CH3_Bead'):
        super(CH3_Bead, self).__init__()

        self.name = name

        bead = mb.Particle(pos=[0.0, 0.0, 0.0], name='_CH3')
        self.add(bead)

        cap_port = mb.Port(anchor=bead, orientation=[0, 0, 1], separation=0.05)
        self.add(cap_port, label='cap')


class Alkane_Bead(mb.Compound):
    def __init__(self, chain_length=3, name='Alkane_Bead'):
        super(Alkane_Bead, self).__init__()

        self.name = name

        terminal_bead = CH3_Bead()
        last_unit = CH2_Bead()
        mb.force_overlap(move_this=terminal_bead,
                         from_positions=terminal_bead['cap'],
                         to_positions=last_unit['up'])
        self.add(last_unit, label='_A[$]')
        self.add(terminal_bead, label='up-cap')
        for _ in range(chain_length - 3):
            current_unit = CH2_Bead()
            mb.force_overlap(move_this=current_unit,
                             from_positions=current_unit['up'],
                             to_positions=last_unit['down'])
            self.add(current_unit, label='_A[$]')
            last_unit = current_unit
        terminal_bead = CH3_Bead()
        mb.force_overlap(move_this=terminal_bead,
                         from_positions=terminal_bead['cap'],
                         to_positions=last_unit['down'])
        self.add(terminal_bead, label='down-cap')
        if chain_length < 3:
            print("Note, the shortest chain this function will make is 3")


class isoButane(mb.Compound):
    def __init__(self, name='isoButane'):
        super(isoButane, self).__init__()

        self.name = name

        CH_1_1 = mb.Particle(pos=[0.0, 0.0, 0.0], name='_HC')
        CH3_1_1 = mb.Particle(pos=[0, 0.0, 0.0], name='_CH3')
        CH3_1_2 = mb.Particle(pos=[0, 0.0, 0.0], name='_CH3')
        CH3_1_3 = mb.Particle(pos=[0, 0, 0.0], name='_CH3')
        self.add([CH_1_1, CH3_1_1, CH3_1_2, CH3_1_3])

        port_1_CH_1_1 = mb.Port(anchor=CH_1_1, orientation=[-0.1, 0, 0], separation=0.05)
        port_2_CH_1_1 = mb.Port(anchor=CH_1_1, orientation=[0, 0.1, 0], separation=0.05)
        port_3_CH_1_1 = mb.Port(anchor=CH_1_1, orientation=[0, -0.1, 0], separation=0.05)
        port_1_CH3_1_1 = mb.Port(anchor=CH3_1_1, orientation=[-0.1, 0, 0], separation=0.05)
        port_1_CH3_1_2 = mb.Port(anchor=CH3_1_2, orientation=[-0.1, 0, 0], separation=0.05)
        port_1_CH3_1_3 = mb.Port(anchor=CH3_1_3, orientation=[-0.1, 0, 0], separation=0.05)

        self.add(port_1_CH_1_1, label='left')
        self.add(port_2_CH_1_1, label='right')
        self.add(port_3_CH_1_1, label='down')
        self.add(port_1_CH3_1_1, label='left_1')
        self.add(port_1_CH3_1_2, label='left_2')
        self.add(port_1_CH3_1_3, label='left_3')

        mb.force_overlap(move_this=CH3_1_1,
                         from_positions=self['left_1'],
                         to_positions=self['left'])
        mb.force_overlap(move_this=CH3_1_2,
                         from_positions=self['left_2'],
                         to_positions=self['right'])
        mb.force_overlap(move_this=CH3_1_3,
                         from_positions=self['left_3'],
                         to_positions=self['down'])


class ethane(mb.Compound):
    def __init__(self, name='ethane'):
        super(ethane, self).__init__()

        self.name = name

        CH3_1_1 = mb.Particle(pos=[0, 0.0, 0.0], name='_CH3')
        CH3_1_2 = mb.Particle(pos=[0, 0.0, 0.0], name='_CH3')
        self.add([CH3_1_1, CH3_1_2])

        port_1_CH3_1_1 = mb.Port(anchor=CH3_1_1, orientation=[-0.1, 0, 0], separation=0.05)
        port_1_CH3_1_2 = mb.Port(anchor=CH3_1_2, orientation=[-0.1, 0, 0], separation=0.05)

        self.add(port_1_CH3_1_1, label='left_1')
        self.add(port_1_CH3_1_2, label='left_2')

        mb.force_overlap(move_this=CH3_1_1,
                         from_positions=self['left_1'],
                         to_positions=self['left_2'])
