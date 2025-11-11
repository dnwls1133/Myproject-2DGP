from event_to_string import event_to_string
import machine.events as events
class StateMachine:
    def __init__(self, start_state,state_transitions):
        self.cur_state = start_state
        self.state_transitions = state_transitions
        self.cur_state.enter(('START',None))
        self.previous_state = None

    def update(self):
        self.cur_state.do()

    def handle_state_event(self, state_event):
        if state_event == ('RETURN', None):
            if self.previous_state is not None:
                self.cur_state.exit(state_event)
                next_state = self.previous_state
                next_state.enter(state_event)
                print(f'State Transition: {self.cur_state.__class__.__name__} -> {next_state.__class__.__name__} by RETURN')
                self.cur_state = next_state
            return

        for check_event in self.state_transitions[self.cur_state].keys():
            next_state = self.state_transitions[self.cur_state][check_event]

            if check_event(state_event):
                self.cur_state.exit(state_event)

                # 상태 전환 전에 이전 상태 저장
                self.previous_state = self.cur_state

                next_state.enter(state_event)
                print(
                    f'State Transition: {self.cur_state.__class__.__name__} -> {next_state.__class__.__name__} by {event_to_string(state_event)}')

                self.cur_state = next_state
                return

        print(f'처리되지 않은 이벤트 {event_to_string(state_event)} 가 있습니다.')

        # ✅ 강제 전환 메서드 추가
    def force_transition(self, next_state):
        """특정 상태로 강제 전환 (이벤트 없이)"""
        self.cur_state.exit(('FORCE', None))
        print(f'State Transition: {self.cur_state.__class__.__name__} -> {next_state.__class__.__name__} by FORCE')
        self.cur_state = next_state
        self.cur_state.enter(('FORCE', None))
    def draw(self):
        self.cur_state.draw()