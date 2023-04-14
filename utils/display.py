from matplotlib import pyplot as plt
from .path import working_path
import streamlit as st
import statistics, pickle


class Atom:
    """
    Simple class to hold data and compute mean and total of values.
    """

    def __init__(self):
        self._raw = []
        self._mean = []
        self._total = []

    def mean(self):
        self._mean.append(statistics.mean(self._raw) if len(self._raw) > 0 else 0)

    def total(self):
        self._total.append(sum(self._raw))

    def clear(self):
        self._raw.clear()

    def append(self, item):
        self._raw.append(item)

    def mov_avg(self, t):
        values = (
            [0] * (t - len(self._total)) + self._total
            if len(self._total) < t
            else self._total[-t:]
        )
        self._mean.append(statistics.mean(values))


class Structure:
    """
    Class to hold all data
    """

    def __init__(self, path):
        self.ep = 1
        self.successes = 0
        self.losses = Atom()
        self.rewards = Atom()
        self.q_values = Atom()
        self.path = path

    def __iter__(self):
        yield self.losses._raw
        yield self.rewards._mean
        yield self.q_values._mean
        yield self.rewards._raw
        yield self.rewards._total
        yield self.q_values._total

    def round(self):
        self.ep += 1
        self.rewards.mov_avg(20)
        self.rewards.total()
        self.q_values.mean()
        self.q_values.total()
        self.clear()

    def clear(self):
        self.losses.clear()
        self.rewards.clear()
        self.q_values.clear()

    def save(self):
        """Save data in `pickle` file"""
        with open(self.path / f"episode-{self.ep}.pkl", "wb") as file:
            pickle.dump(list(self) + [self.successes], file)
        print(f"Episode {self.ep} saved.")


class Display:

    """
    Class to display data
    """

    Y_LABELS = (
        "Loss per optimization",
        "Average of rewards per episode",
        "Average of max predicted Q value",
        "Rewards per action",
        "Total of rewards per episode",
        "Total of max predicted Q value",
    )

    def __init__(self, stream=True, image=False):
        self.data = Structure(working_path(stream, offset=1) / "recorded-data")
        if stream:  # To display the game and progression of the network's performance
            st.set_page_config(layout="wide")
            self.obs = None
            self.placeholder = st.empty()
        else:  # To display only network's performance
            self.fig, self.axis = plt.subplots(2, 3, figsize=(16, 10))
            self.fig.tight_layout()
            self.axis = self.axis.flatten()

        self.stream = (lambda u: self._stream(u)) if stream else (lambda u: None)
        self.save = (lambda: None) if stream else (lambda: self._save(image))

    def update_axis(self, observation=False):
        for axis, data in zip(self.axis[:-1], self.data):
            axis.plot(range(len(data)), data)
        for label, axis in zip(self.Y_LABELS, self.axis[:-1]):
            axis.set_ylabel(label)
        if observation:
            self.axis[6].imshow(self.obs)
        episodes = self.data.ep
        successes = self.data.successes
        self.fig.suptitle(f"Episode {episodes} | Total of successes = {successes}")

    def _save(self, image=False):
        """Save data in `pickle` file and an image"""
        if image:
            PATH_PLOTS = self.data.path / '..' / 'plots' # Elijah fixed a bug here and defined PATH_PLOTS
            self.update_axis()
            self.fig.tight_layout()
            plt.savefig(PATH_PLOTS / f"episode-{self.data.ep}.png")
            print(f"Figure {self.data.ep} saved.")
            for axis in self.axis:
                axis.cla()
        self.data.save()

    def _stream(self, update_all=False):
        with self.placeholder.container():
            columns = st.columns(3) + st.columns(3) + st.columns(3)
            if update_all:
                data = iter(self.data)
                for i in range(6):
                    columns[i].write(self.Y_LABELS[i])
                    columns[i].line_chart(next(data))
                    columns[i].empty()
            columns[7].image(self.obs, use_column_width=True)
            columns[7].empty()
