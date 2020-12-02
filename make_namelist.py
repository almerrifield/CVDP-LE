import sys
from pathlib import Path

'''

Creates namelist for the CVDP-LE based on ETHZ cmip6 naming conventions
ex. 'ts_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc'

- files are in a single directory with path given by user
- run numbers are padded with leading zeros (up to 2) to achieve numerical order

Outputs list of namelist entrys:
ex.
CCCma r001i1p1f1 | /project/yampa03/clivar_wg_le/canesm2_lens/Amon/*/*historical_rcp85_r1i1p1*.nc | 1950 | 2019 | 1-CCCma


'''

def main():
	try:
		path = Path(sys.argv[1])
	except IndexError:
		print("please specify the path that contains the files after the script command")

	result = []

	for file in path.iterdir():
		if file.suffix == ".nc":
			part = file.name
			run_no = part.split("_")[4]  # gets r.i.p.f.
			r_part, past_i_part = run_no.split("i", 1) # separates r from rest
			rid = r_part.split("r")[1] # gets run id number
			rid = int(rid)
			if rid > 999:
				raise RuntimeError("rid exceeds zero padding.")

			new_run_no = f"r{rid:0>3}i{past_i_part}"

			new_filename=part.replace(run_no, new_run_no)
			if file.name != new_filename:
				file.rename(new_filename)
				print(f"renamed file {file.name} to {new_filename}")

	ind_mapping = dict()
	for file in sorted(list(path.iterdir())):
		if file.suffix == ".nc":
			part = file.name
			mod_name = part.split("_")[2] # selects model id

			# generate index of model ids for last namelist entry
			if mod_name not in ind_mapping:
				ind_mapping[mod_name] = len(ind_mapping)+1
			ind = ind_mapping[mod_name]

			run_no = part.split("_")[4] # selects r.i.p.f. id
			period = part.rsplit("_", 1)[1] # selects time period
			yrStart = period.split("-")[0]
			yrStart = yrStart[:4] # selects starting year YYYY
			yrEnd = period.split("-")[1]
			yrEnd = yrEnd[:4] # selects ending year YYYY
			nl_entry = f"{mod_name} {run_no} | {path}/{part} | {yrStart} | {yrEnd} | {ind}-{mod_name}"
			result.append(nl_entry)
		else:
			print("ignoring: {}".format(file))

	target = "namelist_ENSO_spectra.txt"
	with open(target, "w") as f:
		f.write("\n".join(result))
	print(f"{len(result)} filenames were written to file {target}")


if __name__ == "__main__":
	main()
