import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, MapPin, Mail, Lock, User, Phone, Globe, AlertCircle, CheckCircle } from "lucide-react";
import api from "../api";

const LANGUAGES = ["English","Hindi","Tamil","Telugu","Kannada","Malayalam","Bengali","Marathi","French","German","Japanese","Arabic","Spanish","Chinese"];
const STATES = ["Andhra Pradesh","Assam","Bihar","Delhi","Goa","Gujarat","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Punjab","Rajasthan","Tamil Nadu","Telangana","Uttar Pradesh","West Bengal","Other"];

export default function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ fullName:"", email:"", mobile:"", password:"", confirmPassword:"", language:"", homeState:"" });
  const [showPass, setShowPass] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const validate = () => {
    if (!form.fullName.trim())                        return "Full name is required.";
    if (!form.email.trim() || !form.email.includes("@")) return "Enter a valid email address.";
    if (!/^\d{10}$/.test(form.mobile))                return "Enter a valid 10-digit mobile number.";
    if (form.password.length < 6)                     return "Password must be at least 6 characters.";
    if (form.password !== form.confirmPassword)        return "Passwords do not match.";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    const err = validate();
    if (err) { setError(err); return; }
    setLoading(true);
    try {
      await api.post("/auth/register", { email: form.email, password: form.password, mobile: form.mobile });
      setSuccess("Account created! Redirecting to login...");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      setError(err.userMessage);
    } finally {
      setLoading(false);
    }
  };

  const strength = !form.password ? null
    : form.password.length < 6  ? { label:"Weak",   color:"#ef4444" }
    : form.password.length < 10 ? { label:"Medium", color:"#f59e0b" }
    :                              { label:"Strong", color:"#22c55e" };

  return (
    <div style={S.page}>
      <div style={S.left}>
        <div style={S.lc}>
          <div style={S.logoRow}>
            <div style={S.logoIcon}><MapPin size={32} color="#fff"/></div>
            <div><div style={S.appName}>TourGuide</div><div style={S.appTag}>Smart Tourism Assistant</div></div>
          </div>
          <h1 style={S.heroTitle}>Join Millions of<br/>Happy Travellers</h1>
          <p style={S.heroSub}>Create your free account and get access to real-time travel assistance, safety alerts, local food guides, and much more.</p>
          <div style={S.steps}>
            {[["1","Create your account"],["2","Search your destination"],["3","Explore with confidence"]].map(([n,t]) => (
              <div key={n} style={S.step}><div style={S.stepNum}>{n}</div><span style={{fontSize:14}}>{t}</span></div>
            ))}
          </div>
        </div>
      </div>

      <div style={S.right}>
        <div style={S.card}>
          <h2 style={S.title}>Create Account 🌍</h2>
          <p style={S.sub}>Start your smart travel journey today</p>

          {error   && <div style={S.errBox}><AlertCircle size={15}/> {error}</div>}
          {success && <div style={S.sucBox}><CheckCircle size={15}/> {success}</div>}

          <form onSubmit={handleSubmit} style={S.form}>
            <Field label="Full Name"><Inp icon={<User size={16}/>} name="fullName" placeholder="Enter your full name" value={form.fullName} onChange={handleChange}/></Field>
            <Field label="Email Address"><Inp icon={<Mail size={16}/>} name="email" type="email" placeholder="Enter your email" value={form.email} onChange={handleChange}/></Field>
            <Field label="Mobile Number"><Inp icon={<Phone size={16}/>} name="mobile" type="tel" placeholder="10-digit mobile number" value={form.mobile} onChange={handleChange} maxLength={10}/></Field>

            <div style={S.row}>
              <div style={S.field}>
                <label style={S.label}>Password</label>
                <div style={S.wrap}>
                  <Lock size={16} style={S.icon}/>
                  <input name="password" type={showPass?"text":"password"} placeholder="Min. 6 characters"
                    value={form.password} onChange={handleChange} style={{...S.input,paddingRight:38}}/>
                  <button type="button" onClick={()=>setShowPass(!showPass)} style={S.eye}>{showPass?<EyeOff size={15}/>:<Eye size={15}/>}</button>
                </div>
                {strength && <span style={{fontSize:11,color:strength.color,fontWeight:600,marginTop:4}}>● {strength.label} password</span>}
              </div>
              <div style={S.field}>
                <label style={S.label}>Confirm Password</label>
                <div style={S.wrap}>
                  <Lock size={16} style={S.icon}/>
                  <input name="confirmPassword" type={showConfirm?"text":"password"} placeholder="Re-enter password"
                    value={form.confirmPassword} onChange={handleChange} style={{...S.input,paddingRight:38}}/>
                  <button type="button" onClick={()=>setShowConfirm(!showConfirm)} style={S.eye}>{showConfirm?<EyeOff size={15}/>:<Eye size={15}/>}</button>
                </div>
                {form.confirmPassword && <span style={{fontSize:11,fontWeight:600,marginTop:4,color:form.password===form.confirmPassword?"#22c55e":"#ef4444"}}>
                  {form.password===form.confirmPassword?"✓ Passwords match":"✗ Do not match"}
                </span>}
              </div>
            </div>

            <div style={S.row}>
              <div style={S.field}>
                <label style={S.label}>Preferred Language</label>
                <div style={S.wrap}>
                  <Globe size={16} style={S.icon}/>
                  <select name="language" value={form.language} onChange={handleChange} style={{...S.input,paddingLeft:38}}>
                    <option value="">Select language</option>
                    {LANGUAGES.map(l=><option key={l}>{l}</option>)}
                  </select>
                </div>
              </div>
              <div style={S.field}>
                <label style={S.label}>Home Country / State</label>
                <div style={S.wrap}>
                  <MapPin size={16} style={S.icon}/>
                  <select name="homeState" value={form.homeState} onChange={handleChange} style={{...S.input,paddingLeft:38}}>
                    <option value="">Select state</option>
                    {STATES.map(s=><option key={s}>{s}</option>)}
                  </select>
                </div>
              </div>
            </div>

            <button type="submit" style={S.btn} disabled={loading}>{loading?"Creating Account...":"Create Account"}</button>
          </form>

          <p style={S.bottom}>Already have an account? <Link to="/login" style={S.link}>Sign In</Link></p>
        </div>
      </div>
    </div>
  );
}

function Field({ label, children }) {
  return <div style={{display:"flex",flexDirection:"column",gap:6}}><label style={{fontSize:13,fontWeight:600,color:"#374151"}}>{label}</label>{children}</div>;
}
function Inp({ icon, ...props }) {
  return (
    <div style={{position:"relative",display:"flex",alignItems:"center"}}>
      <span style={{position:"absolute",left:12,color:"#94a3b8",pointerEvents:"none",display:"flex"}}>{icon}</span>
      <input {...props} style={{width:"100%",padding:"11px 14px 11px 38px",border:"1.5px solid #e2e8f0",borderRadius:8,fontSize:14,outline:"none"}}/>
    </div>
  );
}

const S = {
  page:{display:"flex",minHeight:"100vh"},
  left:{flex:1,background:"linear-gradient(135deg,#7c3aed,#2563eb,#0ea5e9)",display:"flex",alignItems:"center",justifyContent:"center",padding:48},
  lc:{maxWidth:400,color:"#fff"},
  logoRow:{display:"flex",alignItems:"center",gap:14,marginBottom:40},
  logoIcon:{width:56,height:56,borderRadius:16,background:"rgba(255,255,255,0.2)",display:"flex",alignItems:"center",justifyContent:"center"},
  appName:{fontSize:22,fontWeight:800},
  appTag:{fontSize:13,color:"rgba(255,255,255,0.75)",marginTop:2},
  heroTitle:{fontSize:34,fontWeight:800,lineHeight:1.25,marginBottom:16},
  heroSub:{fontSize:15,color:"rgba(255,255,255,0.8)",lineHeight:1.7,marginBottom:32},
  steps:{display:"flex",flexDirection:"column",gap:14},
  step:{display:"flex",alignItems:"center",gap:14},
  stepNum:{width:32,height:32,borderRadius:"50%",background:"rgba(255,255,255,0.25)",display:"flex",alignItems:"center",justifyContent:"center",fontWeight:700,fontSize:14,flexShrink:0},
  right:{width:560,display:"flex",alignItems:"center",justifyContent:"center",padding:32,background:"#f8fafc",overflowY:"auto"},
  card:{width:"100%",background:"#fff",borderRadius:20,padding:40,boxShadow:"0 4px 24px rgba(0,0,0,0.08)"},
  title:{fontSize:26,fontWeight:800,color:"#1e293b",marginBottom:6},
  sub:{fontSize:14,color:"#64748b",marginBottom:24},
  errBox:{display:"flex",alignItems:"center",gap:8,background:"#fee2e2",color:"#dc2626",borderRadius:8,padding:"10px 14px",fontSize:13,marginBottom:16},
  sucBox:{display:"flex",alignItems:"center",gap:8,background:"#dcfce7",color:"#16a34a",borderRadius:8,padding:"10px 14px",fontSize:13,marginBottom:16},
  form:{display:"flex",flexDirection:"column",gap:16},
  row:{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16},
  field:{display:"flex",flexDirection:"column",gap:5},
  label:{fontSize:13,fontWeight:600,color:"#374151"},
  wrap:{position:"relative",display:"flex",alignItems:"center"},
  icon:{position:"absolute",left:12,color:"#94a3b8",pointerEvents:"none"},
  input:{width:"100%",padding:"11px 14px 11px 38px",border:"1.5px solid #e2e8f0",borderRadius:8,fontSize:14,outline:"none"},
  eye:{position:"absolute",right:10,background:"none",border:"none",cursor:"pointer",color:"#94a3b8",display:"flex",alignItems:"center"},
  btn:{width:"100%",padding:13,fontSize:15,fontWeight:700,borderRadius:10,border:"none",cursor:"pointer",color:"#fff",background:"linear-gradient(135deg,#7c3aed,#2563eb)",marginTop:4},
  bottom:{textAlign:"center",fontSize:14,color:"#64748b",marginTop:20},
  link:{color:"#2563eb",fontWeight:700},
};
