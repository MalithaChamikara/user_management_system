import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { API_URL } from "@/apiConfig";

// Async thunk to fetch users from the server with a action type of "users/fetchUsers"
// This function will be called when the component mounts or when the user clicks the button to fetch users
export const fetchUsers = createAsyncThunk("users/fetchUsers", async () => {
    try {
        const response = await axios.get(`${API_URL}/users`, {
            headers: {
                Authorization: `Bearer ${sessionStorage.getItem('token')}`
            }
        });
        return response.data;
    } catch (error) {
        return error.message;
    }
})

// Async thunk to delete a user with a action type of "users/deleteUser"
// This function will be called when the user clicks the delete button
export const deleteUser = createAsyncThunk("users/deleteUser", async (id) => {
    try {
        const response = await axios.delete(`${API_URL}/users/${id}`, {
            headers: {
                Authorization: `Bearer ${sessionStorage.getItem('token')}`
            }
        });
        return id; // Return the ID of the deleted user
    } catch (error) {
        return error.message;
    }
})

// Redux slice for user management
// Manages the state of users, including fetching, deleting users
// The slice contains the initial state, reducers, and extra reducers for handling async actions
// The slice is created using createSlice from Redux Toolkit

const userSlice = createSlice({
    name: "users", // Name of the slice
    initialState: {
        users: [],
        searchTerm: '',
        error: null,
        loading: false

    },
    reducers: {
        // reducer to update the search term in the state
        setSearchTerm: (state, action) => {
            state.searchTerm = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            //handle pending state for fetchUsers
            .addCase(fetchUsers.pending, (state) => {
                state.loading = true,
                    state.error = null
            })

            //handle fullfilled state for fetchUsers
            .addCase(fetchUsers.fulfilled, (state, action) => {
                state.loading = false,
                    state.users = action.payload
            })

            // handle rejected state for fetchUsers
            .addCase(fetchUsers.rejected, (state, action) => {
                state.loading = true,
                    state.error = action.error?.message
            })

            //handle fulfilled state for deleteUser
            .addCase(deleteUser.fulfilled, (state, action) => {
                // Remove user from the state using returned UserID
                state.users = state.users.filter((user) => user.UserID !== action.payload)
            })

            //handle rejected state for deletedUser
            .addCase(deleteUser.rejected, (state, action) => {
                state.error = action.error?.message
            })
    }
})

// Export the setSearchTerm action 
export const {setSearchTerm} = userSlice.actions

// Export the reducer
export default userSlice.reducer
