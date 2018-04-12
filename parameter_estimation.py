import random
import agent
from sklearn import linear_model
import numpy as np

radius_max = 1
radius_min = 0.1
angle_max = 1
angle_min = 0.1
level_max = 1
level_min = 0

types = ['l1', 'l2', 'f1', 'f2']


class Parameter:
    def __init__(self, level, angle, radius):
        self.level = level
        self.angle = angle
        self.radius = radius

    def update(self, added_value):
        self.level += added_value[0]
        self.angle += added_value[1]
        self.radius += added_value[2]
        return self


class TypeEstimation:
    def __init__(self, a_type):
        self.type = a_type
        self.probability_history = []
        self.estimation_history = []
        self.action_probability = []

    def add_estimation_history(self,probability,level, angle, radius):
        new_parameter = Parameter(level, angle, radius)
        self.estimation_history.append(new_parameter)
        self.probability_history.append(probability)

    def get_last_probability(self):
        return self.probability_history[len(self.probability_history)-1]

    def get_last_estimation(self):
        return self.estimation_history[len(self.estimation_history)-1]


class ParameterEstimation:

    def __init__(self):


        # P(teta|H)
        self.l1_estimation= TypeEstimation('l1')
        self.l2_estimation = TypeEstimation('l2')
        self.f1_estimation = TypeEstimation('f1')
        self.f2_estimation = TypeEstimation('f2')

        # P(a|H,teta,p)
        self.p_action_parameter_type_l1 = []
        self.p_action_parameter_type_l2 = []
        self.p_action_parameter_type_f1 = []
        self.p_action_parameter_type_f2 = []



    # Initialisation random values for parameters of each type and probability of actions in time step 0

    def estimation_initialisation(self):
        # P(teta|H) in t = 0
        self.l1_estimation.add_estimation_history(round(random.uniform(0, 1), 1),

                                                 round(random.uniform(level_min, level_max), 2),  # 'level'
                                                 round(random.uniform(radius_min, radius_max), 2),  # 'radius'
                                                 round(random.uniform(angle_min, angle_max), 2))  # 'angle'

        self.l2_estimation.add_estimation_history(round(random.uniform(0, 1), 1),
                                                 round(random.uniform(level_min, level_max), 2),  # 'level'
                                                 round(random.uniform(radius_min, radius_max), 2),  # 'radius'
                                                 round(random.uniform(angle_min, angle_max), 2))  # 'angle'

        self.f1_estimation.add_estimation_history(round(random.uniform(0, 1), 1),
                                                 round(random.uniform(level_min, level_max), 2),  # 'level'
                                                 round(random.uniform(radius_min, radius_max), 2),  # 'radius'
                                                 round(random.uniform(angle_min, angle_max), 2))  # 'angle'

        self.f2_estimation.add_estimation_history(round(random.uniform(0, 1), 1),
                                                 round(random.uniform(level_min, level_max), 2),  # 'level'
                                                 round(random.uniform(radius_min, radius_max), 2),  # 'radius'
                                                 round(random.uniform(angle_min, angle_max), 2))  # 'angle'

    # =================Generating  D = (p,f(p)) , f(p) = P(a|H_t_1,teta,p)=========================
    @staticmethod
    def generate_data_for_update_parameter(sim, tmp_agent, data_numbers, action):

        # print '*********************************************************************************'
        # print '******generating data for updating parameter *******'

        D = []  # D= (p,f(p)) , f(p) = P(a|H_t_1,teta,p)

        for i in range(0, data_numbers):

            # Generating random values for parameters
            # tmp_radius = (round(random.uniform(radius_min, radius_max), 2))  # 'radius'
            # tmp_angle = (round(random.uniform(angle_min, angle_max), 2))  # 'angle'
            # tmp_level = (round(random.uniform(level_min, level_max), 2))  # 'level'

            tmp_radius = radius_min + (1.0 *(radius_max - radius_min) / data_numbers) * i
            tmp_angle = angle_min + (1.0 *(angle_max - angle_min) / data_numbers) * i
            tmp_level = level_min + (1.0 *(level_max - level_min) / data_numbers) * i

            tmp_agent.set_parameters(sim, tmp_level, tmp_radius, tmp_angle)

            tmp_agent = sim.move_a_agent(tmp_agent, True)  # f(p)
            p_action = tmp_agent.get_action_probability(action)

            if p_action is not None:
                D.append([tmp_level,tmp_radius, tmp_angle,  p_action])


        # print '******End of generating data for updating parameter *******'
        # print '*********************************************************************************'
        return D

    @staticmethod
    def calculate_gradient_ascent(x_train, y_train, old_parameter):
        # p is parameter estimation value at time step t-1 and D is pair of (p,f(p))
        # f(p) is the probability of action which is taken by unknown agent with true parameters at time step t
        # (implementation of Algorithm 2 in the paper for updating parameter value)

        step_size = 0.05

        reg = linear_model.LinearRegression()

        reg.fit(x_train, y_train)

        gradient = reg.coef_

        new_parameters = old_parameter.update(gradient * step_size)

        if level_min <= new_parameters.level <= level_max or \
                angle_min <= new_parameters.angle<= angle_max or \
                radius_min <= new_parameters.radius <= radius_max :
            return new_parameters

        else:
            return old_parameter

    def bayesian_updating(self, x_train):
        pass

    def calculate_EGO(self,agent_type,time_step):  # Exact Global Optimisation

        multiple_results = 1
        if agent_type.agent_type == 'l1':
            for i in range(0,time_step):
                multiple_results = multiple_results * self.p_action_parameter_type_l1[i]

        if agent_type.agent_type == 'l2':
            self.p_action_parameter_type_l2 = []
        if agent_type.agent_type == 'f1':
            self.p_action_parameter_type_f1 = []

        if agent_type.agent_type == 'f2':
            self.p_action_parameter_type_f2 = []

        return

    def parameter_estimation(self,time_step, cur_agent, sim, action):

        data_numbers = 10

        D = self.generate_data_for_update_parameter(sim, cur_agent, data_numbers, action)

        x_train = []
        y_train = []

        if len(D) == 0:
            return

        # Extract x, y train from generated data
        for i in range(0, data_numbers):
            x_train.append(D[i][0:3])
            y_train.append(D[i][3])

        last_parameters_value = 0

        if cur_agent.agent_type == 'l1':
            last_parameters_value = self.l1_estimation.estimation_history[time_step - 1]

        if cur_agent.agent_type == 'l2':
            last_parameters_value = self.l2_estimation.estimation_history[time_step - 1]

        if cur_agent.agent_type == 'f1':
            last_parameters_value = self.f1_estimation.estimation_history[time_step - 1]

        if cur_agent.agent_type == 'f2':
            last_parameters_value = self.f2_estimation.estimation_history[time_step - 1]

        # parameters value order is : radius , angle, level
        estimated_parameter = self.calculate_gradient_ascent(x_train, y_train, last_parameters_value)
        # D = (p,f(p)) , f(p) = P(a|H_t_1,teta,p)


        ##print '***********************************************************************************************'
        return estimated_parameter

    def update_belief(self,t,agent_type):

        if agent_type == 'l1':
            self.l1_estimation.probability_history.append(self.l1_estimation.probability_history[t - 1] * self.p_action_parameter_type_l1[t - 1])

        if agent_type == 'l2':
            self.l2_estimation.probability_history.append(self.l2_estimation.probability_history[t - 1] * self.p_action_parameter_type_l2[t - 1])

        if agent_type == 'f1':

            self.f1_estimation.probability_history.append(self.f1_estimation.probability_history[t - 1] * self.p_action_parameter_type_f1[t - 1])

        if agent_type == 'f2':
            self.f2_estimation.probability_history.append(self.f2_estimation.probability_history[t - 1] * self.p_action_parameter_type_f2[t - 1])

    def update_internal_state(self):
        t = 0
        #sim = simulator.simulator(map_history[0], initial_items, initial_agents, n, m)

    def nested_list_sum(self, nested_lists):
        if type(nested_lists) == list:
            return np.sum(self.nested_list_sum(sublist) for sublist in nested_lists)
        else:
            return 1

    def UCB_selection(self, time_step, final=False):
        agent_types = [self.p_type_l1,
                       self.p_type_l2,
                       self.p_type_f1,
                       self.p_type_f2]

        # Get the total number of probabilities
        prob_count = self.nested_list_sum(agent_types)

        # Return the mean probability for each type of bandit
        mean_probabilities = [np.mean(i) for i in agent_types]

        # Confidence intervals from standard UCB formula
        cis = [np.sqrt((2 * np.log(prob_count)) / len(agent_types[i]) + 0.01) for i in range(len(agent_types))]

        # Sum together means and CIs
        ucb_values = np.array(mean_probabilities) + np.array(cis)

        # Get max UCB value
        max_index = np.argmax(ucb_values)

        # Determine Agent Type to return
        try:
            if max_index == 0:
                return_agent = ['l1']
            elif max_index == 1:
                return_agent = ['l2']
            elif max_index == 2:
                return_agent = ['f1']
            elif max_index == 3:
                return_agent = ['f2']
            else:
                print('UCB has not worked correctly, defaulting to l1')
                return_agent = ['l1']
        except:
            print('An error has occured in UCB, resorting to l1')
            return_agent = ['f1']

        print('UCB Algorithm returned agent of type: {}'.format(return_agent[0]))

        if final:
            return return_agent
        else:
            return ['f2']

        # nu = 0.5
        # n = 10
        # parameter_diff_sum =0
        # for i in range (3):
        #     parameter_diff_sum += abs(self.parameters_values_l1[i] - self.parameters_values_l1 [i-1])
        # reward = (1/nu) * parameter_diff_sum
        # return ['l1']

    def process_parameter_estimations(self, time_step, main_sim, agent_position,agent_direction, action, agent_index):

        new_parameters_estimation = None
        tmp_sim = main_sim.copy()
        # Start parameter estimation
        selected_types = types #self.UCB_selection(time_step)  # returns l1, l2, f1, f2
        (x, y) = agent_position  # Position in the world e.g. 2,3

        # Estimate the parameters
        for selected_type in selected_types:
            # Generates an Agent object
            tmp_agent = agent.Agent(x, y, agent_direction, selected_type, agent_index)


            # Return new parameters, applying formulae stated in paper Section 5.2 - list of length 3
            new_parameters_estimation = self.parameter_estimation(time_step, tmp_agent, tmp_sim, action)

            # moving temp agent in previous map with new parameters
            tmp_agent.set_parameters(tmp_sim, new_parameters_estimation.level, new_parameters_estimation.radius,
                                     new_parameters_estimation.angle)


            # Runs a simulator object
            tmp_agent = tmp_sim.move_a_agent(tmp_agent)



            # TODO: Always seems to return 0.01, is this right?
            action_prob = tmp_agent.get_action_probability(action)

            # TODO: Does this do anything?
            self.update_internal_state()

            # Determine which list to append new parameter estimation and action prob to
            if selected_type == 'l1':
                self.l1_estimation.estimation_history.append(new_parameters_estimation)
                self.p_action_parameter_type_l1.append(action_prob)

            if selected_type == 'l2':
                self.l2_estimation.estimation_history.append(new_parameters_estimation)
                self.p_action_parameter_type_l2.append(action_prob)

            if selected_type == 'f1':
                self.f1_estimation.estimation_history.append(new_parameters_estimation)
                self.p_action_parameter_type_f1.append(action_prob)

            if selected_type == 'f2':
                self.f2_estimation.estimation_history.append(new_parameters_estimation)
                self.p_action_parameter_type_f2.append(action_prob)

            self.update_belief(time_step, selected_type)

        return new_parameters_estimation
