import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { API_URL } from "@/apiConfig";

export const login = createAsyncThunk('auth/login', async ({ email, password }) => {
    try {
        const response = await axios.post(`${API_URL}/login`, {
            Email: email,
            Password: password
        })
        return response.data.token
    } catch (error) {
        return error.message
    }
})

const authSlice = createSlice({
    name: 'auth',
    initialState: {
        token: null,
        error: null,
        loading: false
    },
    reducers: {
        logout: (state) => {
            state.token = null
            sessionStorage.removeItem('token')
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(login.pending, (state) => {
                state.loading = true
            })

            .addCase(login.fulfilled, (state, action) => {
                state.token = action.payload
                sessionStorage.setItem('token', action.payload)
            })

            .addCase(login.rejected, (state, action) => {
                state.error = action.error?.message
            })
    }
})

export const { logout } = authSlice.actions
export default authSlice.reducer