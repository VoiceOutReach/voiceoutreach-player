import { useRouter } from 'next/router';
import Head from 'next/head';
import { useEffect, useState } from 'react';

export default function VoiceNotePage() {
  const router = useRouter();
  const { id } = router.query;
  const [audioSrc, setAudioSrc] = useState<string | null>(null);
  const [name, setName] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      const parts = (id as string).split('_');
      setName(parts[0]);
      setAudioSrc(`/voices/${id}.mp3`);
    }
  }, [id]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
      <Head>
        <title>Voice Message from VoiceOutReach.ai</title>
      </Head>

      <div className="max-w-md w-full bg-white shadow-xl rounded-2xl p-6 text-center">
        <h1 className="text-2xl font-semibold mb-2">🎧 New Voice Message</h1>
        <p className="mb-4 text-gray-600">
          This voice note was sent to you via <strong>VoiceOutReach.ai</strong>
        </p>

        {audioSrc ? (
          <audio controls autoPlay className="w-full mb-4">
            <source src={audioSrc} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        ) : (
          <p className="text-sm text-gray-400">Loading audio...</p>
        )}

        <a
          href="https://www.linkedin.com/messaging/"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-full shadow transition"
        >
          💬 Reply on LinkedIn
        </a>
      </div>
    </div>
  );
}
