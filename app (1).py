import streamlit as st
import pandas as pd

st.title("🏨 Hostel Room Allocation System")

# Files
students_file = "students.csv"
rooms_file = "rooms.csv"
allocation_file = "allocation.csv"

# Menu
menu = st.sidebar.selectbox(
    "Menu",
    [
        "View Data",
        "Add Student",
        "Add Room",
        "Allocate Rooms",
        "Search Student",
        "Delete Student",
        "Update Student",
        "Room Availability",
        "Unallocated Students",
        "Reset Allocation"
    ]
)

# ---------------- VIEW DATA ----------------
if menu == "View Data":
    st.subheader("📊 Students")
    st.write(pd.read_csv(students_file))

    st.subheader("🏢 Rooms")
    st.write(pd.read_csv(rooms_file))

    st.subheader("🛏️ Allocation")
    st.write(pd.read_csv(allocation_file))

# ---------------- ADD STUDENT ----------------
elif menu == "Add Student":
    st.subheader("➕ Add Student")

    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female"])
    year = st.selectbox("Year", [1, 2, 3, 4])

    if st.button("Add"):
        df = pd.read_csv(students_file)
        new_id = df["ID"].max() + 1 if not df.empty else 1
        df.loc[len(df)] = [new_id, name, gender, year]
        df.to_csv(students_file, index=False)
        st.success("Student Added")

# ---------------- ADD ROOM ----------------
elif menu == "Add Room":
    st.subheader("🏢 Add Room")

    room_no = st.text_input("Room Number")
    capacity = st.number_input("Capacity", min_value=1)

    if st.button("Add"):
        df = pd.read_csv(rooms_file)
        df.loc[len(df)] = [room_no, capacity, 0]
        df.to_csv(rooms_file, index=False)
        st.success("Room Added")

# ---------------- ALLOCATION ----------------
elif menu == "Allocate Rooms":
    st.subheader("🔄 Allocate Rooms")

    if st.button("Allocate"):
        students = pd.read_csv(students_file)
        rooms = pd.read_csv(rooms_file)
        allocation = pd.read_csv(allocation_file)

        for _, student in students.iterrows():
            if student["ID"] in allocation["student_id"].values:
                continue

            for j, room in rooms.iterrows():
                if room["occupied"] < room["capacity"]:
                    allocation.loc[len(allocation)] = [student["ID"], room["room_no"]]
                    rooms.at[j, "occupied"] += 1
                    break

        allocation.to_csv(allocation_file, index=False)
        rooms.to_csv(rooms_file, index=False)
        st.success("Allocation Done")

# ---------------- SEARCH STUDENT ----------------
elif menu == "Search Student":
    st.subheader("🔍 Search Student")

    search = st.text_input("Enter Name or ID")

    if st.button("Search"):
        df = pd.read_csv(students_file)
        result = df[
            df["Name"].str.contains(search, case=False, na=False) |
            df["ID"].astype(str).str.contains(search)
        ]
        st.write(result)

# ---------------- DELETE STUDENT ----------------
elif menu == "Delete Student":
    st.subheader("❌ Delete Student")

    sid = st.number_input("Enter Student ID", step=1)

    if st.button("Delete"):
        df = pd.read_csv(students_file)
        df = df[df["ID"] != sid]
        df.to_csv(students_file, index=False)
        st.success("Deleted")

# ---------------- UPDATE STUDENT ----------------
elif menu == "Update Student":
    st.subheader("✏️ Update Student")

    sid = st.number_input("Enter Student ID", step=1)
    new_name = st.text_input("New Name")

    if st.button("Update"):
        df = pd.read_csv(students_file)
        df.loc[df["ID"] == sid, "Name"] = new_name
        df.to_csv(students_file, index=False)
        st.success("Updated")

# ---------------- ROOM AVAILABILITY ----------------
elif menu == "Room Availability":
    st.subheader("📊 Room Availability")

    rooms = pd.read_csv(rooms_file)
    rooms["available"] = rooms["capacity"] - rooms["occupied"]
    st.write(rooms)

# ---------------- UNALLOCATED STUDENTS ----------------
elif menu == "Unallocated Students":
    st.subheader("⚠️ Unallocated Students")

    students = pd.read_csv(students_file)
    allocation = pd.read_csv(allocation_file)

    unallocated = students[~students["ID"].isin(allocation["student_id"])]
    st.write(unallocated)

# ---------------- RESET ALLOCATION ----------------
elif menu == "Reset Allocation":
    st.subheader("🧹 Reset Allocation")

    if st.button("Reset"):
        pd.DataFrame(columns=["student_id", "room_no"]).to_csv(allocation_file, index=False)

        rooms = pd.read_csv(rooms_file)
        rooms["occupied"] = 0
        rooms.to_csv(rooms_file, index=False)

        st.success("Reset Done")