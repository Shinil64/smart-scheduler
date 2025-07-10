import streamlit as st
import pandas as pd
import random

# 🎯 Page config
st.set_page_config(page_title="Smart Job Scheduler", page_icon="🛠️", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: steelblue;'>🛠️ Smart Job Shop Scheduler</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# 📤 Upload CSV
uploaded_file = st.file_uploader("📤 Upload Job Dataset (CSV format only)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    with st.expander("📋 View Uploaded Job Data"):
        st.dataframe(df.style.set_properties(**{'background-color': '#f0f0f0'}))

    # 📊 Jobs and Machine Setup
    jobs = df.to_dict("records")
    machines = ['M1', 'M2', 'M3']

    # ⚙️ GA Parameters
    POP_SIZE = 10
    GENERATIONS = 30
    MUTATION_RATE = 0.1

    def fitness(schedule):
        machine_times = {m: 0 for m in machines}
        total_completion = 0
        for job, machine in schedule:
            start = machine_times[machine]
            end = start + job['ProcessingTime']
            machine_times[machine] = end
            total_completion += end
        return -total_completion

    def create_individual():
        return [(random.choice(jobs), random.choice(machines)) for _ in jobs]

    def crossover(parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:]

    def mutate(individual):
        for i in range(len(individual)):
            if random.random() < MUTATION_RATE:
                individual[i] = (individual[i][0], random.choice(machines))

    # 🧠 Genetic Algorithm
    with st.spinner("⏳ Running Smart Scheduler..."):
        population = [create_individual() for _ in range(POP_SIZE)]
        for _ in range(GENERATIONS):
            population.sort(key=fitness)
            new_pop = population[:2]
            while len(new_pop) < POP_SIZE:
                p1, p2 = random.sample(population[:5], 2)
                child = crossover(p1, p2)
                mutate(child)
                new_pop.append(child)
            population = new_pop
        best_schedule = population[0]

    # ✅ Show Final Output
    st.success("🎉 Scheduling complete! Here's the optimized schedule:")

    result_df = pd.DataFrame([{
        "Job": job["JobID"],
        "Machine Assigned": machine,
        "Processing Time": job["ProcessingTime"]
    } for job, machine in best_schedule])

    # ⏱ Summary
    total_time = result_df["Processing Time"].sum()
    machine_counts = result_df["Machine Assigned"].value_counts().to_dict()

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📦 Total Jobs Scheduled", len(result_df))
            st.metric("🕒 Total Processing Time", f"{total_time} units")
        with col2:
            st.write("🛠️ Jobs per Machine:")
            st.json(machine_counts)

    # 📊 Final Table
    st.dataframe(result_df.style.set_properties(**{
        'background-color': '#e7f3ff',
        'color': '#003366',
        'border-color': 'black'
    }))

    st.balloons()

else:
    st.info("👈 Please upload a valid CSV file to begin scheduling.")
