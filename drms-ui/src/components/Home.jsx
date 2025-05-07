import React from 'react'

const Home = () => {
  return (
    <div className="bg-gray-700 text-white min-h-screen py-12 px-6 md:px-20">
      {/* Title */}
      <h1 className="text-4xl md:text-6xl font-extrabold mb-6 text-center">
        Digital Resource Management
      </h1>

      {/* Sub-description */}
      <p className="text-gray-300 text-lg md:text-xl text-center max-w-3xl mx-auto mb-12">
        A centralized platform to manage employee data, resources, and digital assets efficiently — designed for teams and organizations that value clarity and control.
      </p>

      {/* Features */}
      <div className="grid gap-8 md:grid-cols-2">
        <FeatureCard
          title="👤 Employee Management"
          description="Add, view, and manage employee details with a user-friendly interface."
        />
        <FeatureCard
          title="📁 Image Upload"
          description="Securely upload images to AWS S3 with real-time UI feedback and preview."
        />
        <FeatureCard
          title="🔍 Query System"
          description="Search and filter uploaded resources efficiently using metadata or filename."
        />
        <FeatureCard
          title="🛡️ Secure Access"
          description="Access files via pre-signed URLs with proper authorization and file validation."
        />
      </div>
    </div>
  );
}

// Reusable feature card component
function FeatureCard({ title, description }) {
  return (
    <div className="bg-gray-800 p-6 rounded-xl shadow-md hover:shadow-lg transition">
      <h2 className="text-2xl font-semibold mb-2">{title}</h2>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}

export default Home