import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, MapPin, Mail, Lock, AlertCircle } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../api";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ identifier: "", password: "" });
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!form.identifier || !form.password) { setError("Please fill in all fields."); return; }
    setLoading(true);
    try {
      const res = await api.post("/auth/login", { email: form.identifier, password: form.password });
      login(res.data.user, res.data.access_token);
      navigate("/home");
    } catch (err) {
      setError(err.userMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={S.page}>
      <div style={S.left}>
        <div style={S.leftContent}>
          <div style={S.logoRow}>
            <div style={S.logoIcon}><MapPin size={32} color="#fff" /></div>
            <div>
              <div style={S.appName}>TourGuide</div>
              <div style={S.appTagline}>Smart Tourism Assistant</div>
            </div>
          </div>
          <h1 style={S.heroTitle}>Explore the World<br />with Confidence</h1>
          <p style={S.heroSub}>Real-time weather, safety alerts, local food, hotel bookings, language support — all in one app.</p>
          <div style={S.features}>
            {["📍 Live Location & Nearby Places","🌦️ Weather Forecasts","🚨 Emergency Safety Alerts","🍲 Local Food & Temple Meals","🏨 Hotel & Transport Booking"].map(f => (
              <div key={f} style={S.featureItem}>{f}</div>
            ))}
          </div>
        </div>
      </div>

      <div style={S.right}>
        <div style={S.card}>
          <h2 style={S.title}>Welcome Back 👋</h2>
          <p style={S.sub}>Sign in to continue your journey</p>

          {error && <div style={S.errorBox}><AlertCircle size={15}/> {error}</div>}

          <form onSubmit={handleSubmit} style={S.form}>
            <div style={S.field}>
              <label style={S.label}>Email / Mobile Number</label>
              <div style={S.wrap}>
                <Mail size={16} style={S.icon}/>
                <input name="identifier" type="text" placeholder="Enter email or mobile"
                  value={form.identifier} onChange={handleChange} style={S.input}/>
              </div>
            </div>

            <div style={S.field}>
              <label style={S.label}>Password</label>
              <div style={S.wrap}>
                <Lock size={16} style={S.icon}/>
                <input name="password" type={showPass ? "text" : "password"} placeholder="Enter your password"
                  value={form.password} onChange={handleChange} style={{...S.input, paddingRight:40}}/>
                <button type="button" onClick={() => setShowPass(!showPass)} style={S.eye}>
                  {showPass ? <EyeOff size={16}/> : <Eye size={16}/>}
                </button>
              </div>
            </div>

            <div style={{textAlign:"right"}}>
              <Link to="/forgot-password" style={S.link}>Forgot Password?</Link>
            </div>

            <button type="submit" style={S.btn} disabled={loading}>
              {loading ? "Signing in..." : "Login"}
            </button>
          </form>

          <div style={S.divider}><span style={S.line}/><span style={S.or}>or</span><span style={S.line}/></div>
          <p style={S.bottom}>New user? <Link to="/signup" style={S.link}>Create Account</Link></p>
        </div>
      </div>
    </div>
  );
}

const S = {
  page:{display:"flex",minHeight:"100vh"},
  left:{flex:1,background:"linear-gradient(135deg,#1d4ed8,#2563eb,#0ea5e9)",display:"flex",alignItems:"center",justifyContent:"center",padding:48},
  leftContent:{maxWidth:420,color:"#fff"},
  logoRow:{display:"flex",alignItems:"center",gap:14,marginBottom:40},
  logoIcon:{width:56,height:56,borderRadius:16,background:"rgba(255,255,255,0.2)",display:"flex",alignItems:"center",justifyContent:"center"},
  appName:{fontSize:22,fontWeight:800},
  appTagline:{fontSize:13,color:"rgba(255,255,255,0.75)",marginTop:2},
  heroTitle:{fontSize:36,fontWeight:800,lineHeight:1.25,marginBottom:16},
  heroSub:{fontSize:15,color:"rgba(255,255,255,0.8)",lineHeight:1.7,marginBottom:32},
  features:{display:"flex",flexDirection:"column",gap:10},
  featureItem:{background:"rgba(255,255,255,0.12)",borderRadius:8,padding:"10px 16px",fontSize:14,fontWeight:500},
  right:{width:480,display:"flex",alignItems:"center",justifyContent:"center",padding:32,background:"#f8fafc"},
  card:{width:"100%",background:"#fff",borderRadius:20,padding:40,boxShadow:"0 4px 24px rgba(0,0,0,0.08)"},
  title:{fontSize:26,fontWeight:800,color:"#1e293b",marginBottom:6},
  sub:{fontSize:14,color:"#64748b",marginBottom:24},
  errorBox:{display:"flex",alignItems:"center",gap:8,background:"#fee2e2",color:"#dc2626",borderRadius:8,padding:"10px 14px",fontSize:13,marginBottom:16},
  form:{display:"flex",flexDirection:"column",gap:18},
  field:{display:"flex",flexDirection:"column",gap:6},
  label:{fontSize:13,fontWeight:600,color:"#374151"},
  wrap:{position:"relative",display:"flex",alignItems:"center"},
  icon:{position:"absolute",left:12,color:"#94a3b8",pointerEvents:"none"},
  input:{width:"100%",padding:"11px 14px 11px 38px",border:"1.5px solid #e2e8f0",borderRadius:8,fontSize:14,outline:"none"},
  eye:{position:"absolute",right:12,background:"none",border:"none",cursor:"pointer",color:"#94a3b8",display:"flex",alignItems:"center"},
  btn:{width:"100%",padding:13,fontSize:15,fontWeight:700,borderRadius:10,border:"none",color:"#fff",cursor:"pointer",background:"linear-gradient(135deg,#2563eb,#0ea5e9)"},
  divider:{display:"flex",alignItems:"center",gap:12,margin:"20px 0"},
  line:{flex:1,height:1,background:"#e2e8f0"},
  or:{fontSize:13,color:"#94a3b8"},
  bottom:{textAlign:"center",fontSize:14,color:"#64748b"},
  link:{color:"#2563eb",fontWeight:600,fontSize:13},
};
