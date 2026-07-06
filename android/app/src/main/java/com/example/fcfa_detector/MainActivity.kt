package com.example.fcfa_detector

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.example.fcfa_detector.databinding.ActivityMainBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.ByteArrayOutputStream

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private var selectedImageUri: Uri? = null
    private var selectedBitmap: Bitmap? = null

    private val pickImageLauncher = registerForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        if (uri != null) {
            selectedImageUri = uri
            binding.photoPreview.setImageURI(uri)
            Toast.makeText(this, "Image sélectionnée", Toast.LENGTH_SHORT).show()
        }
    }

    private val takePhotoLauncher = registerForActivityResult(ActivityResultContracts.TakePicturePreview()) { bitmap ->
        if (bitmap != null) {
            selectedBitmap = bitmap
            binding.photoPreview.setImageBitmap(bitmap)
            Toast.makeText(this, "Photo capturée", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.selectImageButton.setOnClickListener {
            pickImageLauncher.launch("image/*")
        }

        binding.takePhotoButton.setOnClickListener {
            takePhotoLauncher.launch(null)
        }

        binding.sendButton.setOnClickListener {
            val imageUri = selectedImageUri
            val bitmap = selectedBitmap
            if (imageUri == null && bitmap == null) {
                Toast.makeText(this, "Sélectionnez d’abord une image", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val bytes = if (bitmap != null) bitmapToBytes(bitmap) else readBytesFromUri(imageUri!!)
            sendImageToApi(bytes)
        }
    }

    private fun bitmapToBytes(bitmap: Bitmap): ByteArray {
        val stream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 90, stream)
        return stream.toByteArray()
    }

    private fun readBytesFromUri(uri: Uri): ByteArray {
        val inputStream = contentResolver.openInputStream(uri)
        return inputStream?.readBytes() ?: ByteArray(0)
    }

    private fun sendImageToApi(bytes: ByteArray) {
        val client = OkHttpClient()
        val requestBody = bytes.toRequestBody("image/jpeg".toMediaTypeOrNull())
        val request = Request.Builder()
            .url("https://your-api-url.com/predict-image")
            .post(requestBody)
            .build()

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val response = client.newCall(request).execute()
                val responseBody = response.body?.string() ?: ""
                withContext(Dispatchers.Main) {
                    binding.resultText.text = responseBody
                    Toast.makeText(this@MainActivity, "Analyse terminée", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    binding.resultText.text = "Erreur : ${e.message}"
                }
            }
        }
    }
}
