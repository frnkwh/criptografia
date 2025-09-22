/**
  AES encryption/decryption demo program using OpenSSL EVP APIs
  gcc -Wall aes_file.c -o aes_file -lcrypto

  Modified to read input from a .txt file and write encrypted/decrypted output to files.
Usage: ./aes_file <key> <input_file.txt>
Outputs: output.enc (encrypted), output.dec.txt (decrypted)
Public domain code.
Original by Saju Pillai (saju.pillai@gmail.com), modified for file I/O.
 **/

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <openssl/evp.h>
#include <openssl/aes.h>

/**
 * Create a 256-bit key and IV using the supplied key_data. Salt can be added for taste.
 * Fills in the encryption and decryption ctx objects and returns 0 on success
 */
int aes_init(unsigned char *key_data, int key_data_len, unsigned char *salt, EVP_CIPHER_CTX *e_ctx, 
		EVP_CIPHER_CTX *d_ctx)
{
	int i, nrounds = 5;
	unsigned char key[32], iv[32];

	i = EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha1(), salt, key_data, key_data_len, nrounds, key, iv);
	if (i != 32) {
		printf("Key size is %d bits - should be 256 bits\n", i);
		return -1;
	}

	EVP_CIPHER_CTX_init(e_ctx);
	EVP_EncryptInit_ex(e_ctx, EVP_aes_256_cbc(), NULL, key, iv);
	EVP_CIPHER_CTX_init(d_ctx);
	EVP_DecryptInit_ex(d_ctx, EVP_aes_256_cbc(), NULL, key, iv);

	return 0;
}

/**
 * Encrypt *len bytes of data
 * All data going in & out is considered binary (unsigned char[])
 */
unsigned char *aes_encrypt(EVP_CIPHER_CTX *e, unsigned char *plaintext, int *len)
{
	int c_len = *len + AES_BLOCK_SIZE, f_len = 0;
	unsigned char *ciphertext = malloc(c_len);

	EVP_EncryptInit_ex(e, NULL, NULL, NULL, NULL);
	EVP_EncryptUpdate(e, ciphertext, &c_len, plaintext, *len);
	EVP_EncryptFinal_ex(e, ciphertext + c_len, &f_len);

	*len = c_len + f_len;
	return ciphertext;
}

/**
 * Decrypt *len bytes of ciphertext
 */
unsigned char *aes_decrypt(EVP_CIPHER_CTX *e, unsigned char *ciphertext, int *len)
{
	int p_len = *len, f_len = 0;
	unsigned char *plaintext = malloc(p_len);

	EVP_DecryptInit_ex(e, NULL, NULL, NULL, NULL);
	EVP_DecryptUpdate(e, plaintext, &p_len, ciphertext, *len);
	EVP_DecryptFinal_ex(e, plaintext + p_len, &f_len);

	*len = p_len + f_len;
	return plaintext;
}

/**
 * Read file into a buffer
 */
unsigned char *read_file(const char *filename, int *len)
{
	FILE *fp = fopen(filename, "rb");
	if (!fp) {
		printf("Error: Cannot open input file %s\n", filename);
		return NULL;
	}

	// Get file size
	fseek(fp, 0, SEEK_END);
	*len = ftell(fp);
	fseek(fp, 0, SEEK_SET);

	// Allocate buffer and read file
	unsigned char *buffer = malloc(*len);
	if (!buffer) {
		printf("Error: Memory allocation failed\n");
		fclose(fp);
		return NULL;
	}

	size_t read_bytes = fread(buffer, 1, *len, fp);
	fclose(fp);

	if (read_bytes != *len) {
		printf("Error: Failed to read entire file\n");
		free(buffer);
		return NULL;
	}

	return buffer;
}

/**
 * Write buffer to file
 */
int write_file(const char *filename, unsigned char *data, int len)
{
	FILE *fp = fopen(filename, "wb");
	if (!fp) {
		printf("Error: Cannot open output file %s\n", filename);
		return -1;
	}

	size_t written = fwrite(data, 1, len, fp);
	fclose(fp);

	if (written != len) {
		printf("Error: Failed to write entire output to %s\n", filename);
		return -1;
	}

	return 0;
}

void log_step(const char *step, double duration, const char *file) {
	printf("{\"step\":\"%s\",\"duration\":%f,\"file\":\"%s\"}\n", step, duration, file);
}

void get_base_filename(const char *path, char *basename) {
	const char *slash = strrchr(path, '/');       // last '/'
	const char *name = slash ? slash + 1 : path; // move past '/' or use whole string
	strcpy(basename, name);

	// remove extension if present
	char *dot = strrchr(basename, '.');
	if (dot) *dot = '\0';
}

int main(int argc, char **argv) {
	if (argc != 3) {
		printf("Usage: %s <key> <input_file.txt>\n", argv[0]);
		return -1;
	}

	const char *key_data = argv[1];
	const char *input_file = argv[2];

	/* Get base filename for logging */
	char file_name[256];
	get_base_filename(input_file, file_name);

	EVP_CIPHER_CTX *en = EVP_CIPHER_CTX_new();
	EVP_CIPHER_CTX *de = EVP_CIPHER_CTX_new();
	if (!en || !de) {
		printf("Error: Failed to create EVP contexts\n");
		return -1;
	}

	unsigned int salt[] = {12345, 54321};
	if (aes_init((unsigned char *)key_data, strlen(key_data), (unsigned char *)&salt, en, de)) {
		printf("Couldn't initialize AES cipher\n");
		EVP_CIPHER_CTX_free(en);
		EVP_CIPHER_CTX_free(de);
		return -1;
	}

	int len;
	unsigned char *input_data = read_file(input_file, &len);
	if (!input_data) {
		EVP_CIPHER_CTX_free(en);
		EVP_CIPHER_CTX_free(de);
		return -1;
	}

	/* --- Encrypt and time it --- */
	clock_t start = clock();
	unsigned char *ciphertext = aes_encrypt(en, input_data, &len);
	clock_t end = clock();
	double enc_time = (double)(end - start) / CLOCKS_PER_SEC;
	log_step("encryption", enc_time, file_name);

	if (write_file("outs/encryptedAES.txt", ciphertext, len)) {
		printf("Error writing encrypted file\n");
		free(input_data);
		free(ciphertext);
		EVP_CIPHER_CTX_free(en);
		EVP_CIPHER_CTX_free(de);
		return -1;
	}

	/* --- Decrypt and time it --- */
	int dec_len = len;
	start = clock();
	unsigned char *decrypted = aes_decrypt(de, ciphertext, &dec_len);
	end = clock();
	double dec_time = (double)(end - start) / CLOCKS_PER_SEC;
	log_step("decryption", dec_time, file_name);

	if (write_file("outs/decryptedAES.txt", decrypted, dec_len)) {
		printf("Error writing decrypted file\n");
		free(input_data);
		free(ciphertext);
		free(decrypted);
		EVP_CIPHER_CTX_free(en);
		EVP_CIPHER_CTX_free(de);
		return -1;
	}

	/* Clean up */
	free(input_data);
	free(ciphertext);
	free(decrypted);
	EVP_CIPHER_CTX_free(en);
	EVP_CIPHER_CTX_free(de);

	return 0;
}

