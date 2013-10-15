# create directory structure
# use template and inputs on file names to create reduction scripts

def mkdirectories():
    return

def mktable_helper(tablename, auto=True, rawdir="./"):
    import obstable
    import os.path
    if auto:
        from astrodata import AstroData
        
    # Create an ObsTable.  If the file already exists on disk,
    # then read it.  Otherwise, leave it empty.
    # Error handling: If the file exists but there's an read error,
    # raise, otherwise assume that you are creating a new file.
    table = obstable.ObsTable(tablename)
    try:
        table.read_table()
    except IOError:
        if os.path.exists(tablename):
            print "Error reading table %s\n" % tablename
            raise
    
    # Start the prompting the user and the data for the information
    # that needs to go in the table.
    
    user_not_done = True
    while user_not_done:
        user_inputs = {}
        if auto:
            filename_not_known = True
        
        # Get list of prompts for user or data supplied information.
        req_input_list = get_req_input_list()
        
        # Loop through record elements
        for input_request in req_input_list:
            if (not input_request['in_hdr'] or not auto):
                # prompt the user
                input_value = raw_input(input_request['prompt'])
                
                # Assume that the user has a brain.
                # Probe only the first file in 'filerange' since all the
                # files in 'filerange' should be similar.
                #
                # Once we know the name of the first MEF file, open it
                # and keep it open until we're done requesting inputs
                # (instead of opening and closing it every time).
                if auto and filename_not_known:
                    if user_inputs.has_key('root') and user_inputs.has_key('filerange'):
                        # parse filerange, build filename (with rawdir path)
                        filenumbers = parse_filerange(user_inputs['filerange'])
                        filename = "%sS%04d.fits" % (user_inputs['root'], filenumbers[0])
                        filename = os.path.join(rawdir,filename)

                        # open ad
                        ad = AstroData(filename)                        
                        filename_not_known = False                    
            else:
                
                # get value from header
                input_value = query_header(ad, input_request['id'])
                
            user_inputs[input_request['id']] = input_value
        
        if auto:
            ad.close()
                
        # Create record
        new_record = create_record(user_inputs)
        
        # Append to table
        table.add_record_to_table(new_record)
        
        # Prompt user: add another entry?
        answer = raw_input('Add another entry (y/n)')
        user_not_done = ((answer=='y') or False)
    
    # All the info is now in the ObsTable.
    # Write the ObsTable to disk and close everything, we're done.
    table.write_table()
    
    return

def mkscript():
    return


#--------------------

def get_req_input_list():
    # target means Science target, eg. a flat is associated
    # to "this" science target, hence cannot be in header.
    target_prompt = {'prompt': 'Name of target',
                     'in_hdr': False,
                     'id': 'targetname'}
    root_prompt = {'prompt': 'File root name (e.g. S201202012)',
                   'in_hdr': False,
                   'id': 'rootname'}
    filerange_prompt = {'prompt': 'filerange string (e.g. 201-205)',
                        'in_hdr': False,
                        'id': 'filerange'}
    applyto_prompt = {'prompt': 'Applies to (e.g. Science)',
                      'in_hrd': False,
                      'id': 'applyto'}
    datatype_prompt = {'prompt': 'Type of observation (e.g. Flat)',
                       'in_hdr': False,
                       'id': 'datatype'}
    band_prompt = {'prompt': 'Band',
                   'in_hdr': True,
                   'id': 'band'}
    grism_prompt = {'prompt': 'Grism',
                    'in_hdr': True,
                    'id': 'grism'}
    exptime_prompt = {'prompt': 'Exposure Time',
                      'in_hdr': True,
                      'id': 'exptime'}
    lnrs_prompt = {'prompt': 'LNRS',
                   'in_hdr': True,
                   'id': 'lnrs'}
    rdmode_prompt = {'prompt': 'Read mode (e.g. Faint, Bright)',
                     'in_hdr': True,
                     'id': 'rdmode'}
    return [root_prompt, filerange_prompt, applyto_prompt, 
                      datatype_prompt, target_prompt, band_prompt, 
                      grism_prompt, exptime_prompt, lnrs_prompt,
                      rdmode_prompt]

def query_header(ad, requested_input):
    # warning: might not be efficient if the descriptor system is slow
    # might have to change to if-elif sequence.  (but it's kinda cool
    # looking this way.)
    return {
        'targetname' : ad.object().as_str(),
        'band'       : ad.filter_name(pretty=True).as_str(),
        'grism'      : ad.disperser(pretty=True).as_str(),
        'exptime'    : ad.exposure_time().as_float(),
        'lnrs'       : ad.phu_get_key_value('LNRS'),
        'rdmode'     : ad.read_mode(pretty=True).as_str() 
    }[requested_input]
    
def create_record(user_inputs):
    import obstable
    
    record = obstable.ObsRecord()
    record.targetname = user_inputs['targetname']
    record.rootname = user_inputs['rootname']
    record.band = user_inputs['band']
    record.grism = user_inputs['grism']
    record.datatype = user_inputs['datatype']
    record.applyto = user_inputs['applyto']
    record.filerange = user_inputs['filerange']
    record.exptime = float(user_inputs['exptime'])
    record.lnrs = integer(user_inputs['lnrs'])
    record.rdmode = user_inputs['rdmode']
    
    return record

def parse_filerange(filerange):
    # Parse strings like this.  
    #    210-214
    #    215
    #    216,217
    #    218-221,223-225
    filenumbers=[]
    ranges = filerange.split(',')
    for range in ranges:
        boundaries = range.split('-')
        if len(boundaries) == 1:
            filenumbers.append(int(boundaries[0]))
        elif len(boundaries) == 2:
            n = int(boundaries[0])
            while n <= int(boundaries[1]):
                filenumbers.append(n)
                n+=1
        else:
            raise RuntimeError
    
    return filenumbers
