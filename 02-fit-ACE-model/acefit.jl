##
using ACE1pack
data = JuLIP.read_extxyz("master_add_surfaces_GBs.xyz")
r0 = 2.55
ACE_B = ace_basis(species = [:Cu],
                  N = 3,
                  maxdeg = 6,
                  rcut = 5.5,
                  r0 = r0,
                  rin = 0.6 * r0, pin = 2);
Bpair = pair_basis(species = [:Cu],
                   r0 = r0,
                   maxdeg = 6,
                   rcut = 7.0)
B = JuLIP.MLIPs.IPSuperBasis([Bpair, ACE_B]);
Vref = OneBody(:Cu => 3.51)
weights = Dict(
        "bulk_Cu" => Dict("E" => 20.0, "F" => 5.0 , "V" => 3.0 ),
        "bulk_vac_images" => Dict("E" => 60.0, "F" => 15.0 , "V" => 10.0 ),
        "isolated_atom" => Dict("E" => 10.0,"F" => 5.0,"V" => 2.0),
        "fcc111_3_3_3_vac10" => Dict("E" => 20.0,"F" => 5.0,"V" => 2.0),
        "fcc111_2_2_2_vac10" => Dict("E" => 20.0,"F" => 5.0,"V" => 2.0),
        "fcc111_4_4_4_vac10" => Dict("E" => 20.0,"F" => 5.0,"V" => 2.0),
        "fcc111_5_5_5_vac10" => Dict("E" => 20.0,"F" => 5.0,"V" => 2.0),
        "twist_001" => Dict("E" => 40.0,"F" => 5.0,"V" => 2.0),
        "tilt_GB_140" => Dict("E" => 40.0,"F" => 5.0,"V" => 2.0),
        "tilt_GB_130" => Dict("E" => 40.0,"F" => 5.0,"V" => 2.0),
        "tilt_GB_120" => Dict("E" => 40.0,"F" => 5.0,"V" => 2.0)
        );
##
train = [ACE1pack.AtomsData(t,"energy","forces","stress",weights,Vref) for t in data]
A, Y, W = ACEfit.linear_assemble(train, B);
##
solver_type = :lsqr
smoothness_prior = true

if solver_type == :lsqr
	solver = Dict(
        	"type" => "LSQR",
        	"damp" => 1e-2,
        	"atol" => 1e-6)
elseif solver_type == :rrqr
	solver = Dict(
        	"type" => "RRQR",
        	"tol" => 1e-5)
elseif solver_type == :brr
	solver = Dict(
        	"type" => "BRR",
		"tol" => 1e-3)
elseif solver_type == :ard
	solver= Dict(
         	"type" => "ARD",
         	"tol" => 1e-3,
         	"threshold_lambda" => 10000)
end
if smoothness_prior
    using LinearAlgebra
    q = 3.0
    solver["P"] = Diagonal(vcat(ACE1.scaling.(B.BB, q)...))
end
solver = ACEfit.create_solver(solver)
results = ACEfit.linear_solve(solver, A, Y)
potential = JuLIP.MLIPs.SumIP(Vref, JuLIP.MLIPs.combine(B, results["C"]))
##
@info("Training Error Table")
ACE1pack.linear_errors(train, potential);

save_dict("./copper_gb.json", Dict("IP" => write_dict(potential)))
ACE1pack.ExportMulti.export_ACE("./copper_gb.yace", potential; export_pairpot_as_table=true)
